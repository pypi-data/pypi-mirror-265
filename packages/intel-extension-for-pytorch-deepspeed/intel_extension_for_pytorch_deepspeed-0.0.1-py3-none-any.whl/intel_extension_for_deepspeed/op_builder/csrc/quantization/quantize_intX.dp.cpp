// Copyright (c) Microsoft Corporation.
// SPDX-License-Identifier: Apache-2.0

// DeepSpeed Team

#include <sycl/sycl.hpp>
#include <dpct/dpct.hpp>
#include <assert.h>
#include "memory_access_utils.h"
#include <cmath>

template <typename T, int N>
struct alignas(sizeof(T) * N) AlignedArray {
    using Element = T;
    static const int kElements = N;

    AlignedArray() {}

    AlignedArray(const T& rhs)
    {
#pragma unroll
        for (int idx = 0; idx < kElements; ++idx) { this->at(idx) = rhs; }
    }

    T& operator[](int offset)
    {
        return reinterpret_cast<T&>(this->buffer[offset]);
    }

    const T& operator[](int offset) const
    {
        return reinterpret_cast<const T&>(this->buffer[offset]);
    }

    T& at(int offset) { return reinterpret_cast<T&>(this->buffer[offset]); }

    const T& at(int offset) const
    {
        return reinterpret_cast<const T&>(this->buffer[offset]);
    }

    AlignedArray<T, N> operator+(const AlignedArray<T, N>& rhs) const
    {
        AlignedArray<T, N> ret;

#pragma unroll
        for (int idx = 0; idx < kElements; ++idx) { ret[idx] = this->at(idx) + rhs.at(idx); }

        return ret;
    }

    __dpct_inline__ void clear()
    {
#pragma unroll
        for (int idx = 0; idx < kElements; ++idx) { this->at(idx) = Element(0); }
    }

    Element buffer[N];
};

template <typename T>
struct reduce_max {
    __dpct_inline__ T operator()(const T& lhs, const T& rhs)
    {
        return lhs > rhs ? lhs : rhs;
    }
};

template <typename T>
struct reduce_min {
    __dpct_inline__ T operator()(const T& lhs, const T& rhs)
    {
        return lhs < rhs ? lhs : rhs;
    }
};

template <typename T, int N>
struct subtract {
    __dpct_inline__ AlignedArray<T, N> operator()(const AlignedArray<T, N>& lhs, const T& rhs)
    {
        AlignedArray<T, N> ret;

#pragma unroll
        for (int idx = 0; idx < N; ++idx) { ret[idx] = lhs[idx] - rhs; }

        return ret;
    }
};

template <typename T, int N>
struct plus {
    __dpct_inline__ AlignedArray<T, N> operator()(const AlignedArray<T, N>& lhs, const T& rhs)
    {
        AlignedArray<T, N> ret;

#pragma unroll
        for (int idx = 0; idx < N; ++idx) { ret[idx] = lhs[idx] + rhs; }

        return ret;
    }
};

template <typename T, int N>
struct multiply {
    __dpct_inline__ AlignedArray<T, N> operator()(const AlignedArray<T, N>& lhs, const T& rhs)
    {
        AlignedArray<T, N> ret;

#pragma unroll
        for (int idx = 0; idx < N; ++idx) { ret[idx] = lhs[idx] * rhs; }

        return ret;
    }
};

template <typename T, int N>
struct clamp {
    __dpct_inline__ AlignedArray<T, N> operator()(const AlignedArray<T, N>& lhs,
                                                  const T& min_val,
                                                  const T& max_val)
    {
        AlignedArray<T, N> ret;

#pragma unroll
        for (int idx = 0; idx < N; ++idx) {
            ret[idx] = reduce_max<T>()(reduce_min<T>()(lhs[idx], max_val), min_val);
        }

        return ret;
    }
};

template <typename T, int N>
struct round_int;

template <int N>
struct round_int<sycl::half, N> {
    __dpct_inline__ AlignedArray<sycl::half, N> operator()(const AlignedArray<sycl::half, N>& lhs)
    {
        AlignedArray<sycl::half, N> ret;

#pragma unroll
        for (int idx = 0; idx < N; ++idx) { ret[idx] = hrint(lhs[idx]); }

        return ret;
    }
};

template <typename T, int N>
struct divide {
    __dpct_inline__ AlignedArray<T, N> operator()(const AlignedArray<T, N>& lhs, const T& rhs)
    {
        AlignedArray<T, N> ret;

#pragma unroll
        for (int idx = 0; idx < N; ++idx) { ret[idx] = lhs[idx] / rhs; }

        return ret;
    }
};

template <typename T, int N, typename Reducer>
__dpct_inline__ T to_scalar(const AlignedArray<T, N>& data)
{
    Reducer re;
    T res = data[0];

#pragma unroll
    for (int idx = 1; idx < N; ++idx) { res = re(res, data[idx]); }

    return res;
}

template <int N>
__dpct_inline__ AlignedArray<sycl::half, N * 2> int4_to_half(const AlignedArray<uint8_t, N>& data)
{
    AlignedArray<sycl::half, N * 2> ret;

#pragma unroll
    for (int idx = 0; idx < N * 2; idx += 2) {
        ret[idx] = sycl::half(int(data[idx / 2] >> 4));
        ret[idx + 1] = sycl::half(int(data[idx / 2] & 0xf));
    }

    return ret;
}

void dequantize_int4_to_half(uint8_t* data_in,
                             sycl::half* data_out,
                             sycl::half* scale_buffer,
                             sycl::half* min_val_buffer,
                             int num_group,
                             int group_size)
{
    auto item_ct1 = sycl::ext::oneapi::experimental::this_nd_item<3>();
    using AccessType = AlignedArray<uint8_t, 4>;
    using AccessTypeOut = AlignedArray<sycl::half, 8>;

    for (int idx = item_ct1.get_local_id(2) + item_ct1.get_group(2) * item_ct1.get_local_range(2);
         idx < num_group * group_size / 8;
         idx += item_ct1.get_local_range(2) * item_ct1.get_group_range(2)) {
        int id_group = idx / (group_size / 8);
        AccessType value = reinterpret_cast<AccessType*>(data_in)[idx];
        sycl::half scale = scale_buffer[id_group];
        sycl::half min_value = min_val_buffer[id_group];

        AccessTypeOut output = int4_to_half(value);
        output = divide<sycl::half, 8>()(output, scale);
        output = plus<sycl::half, 8>()(output, min_value);

        reinterpret_cast<AccessTypeOut*>(data_out)[idx] = output;
    }
}

void launch_dequantize_int4_to_half_experimental(uint8_t* data_in,
                                                 sycl::half* data_out,
                                                 sycl::half* scale_buffer,
                                                 sycl::half* min_val_buffer,
                                                 int num_group,
                                                 int group_size,
                                                 dpct::queue_ptr stream)
{
    int num_warp = num_group / 4;
    int num_block = num_warp / 8;  // 256 trd / block

    {
        dpct::has_capability_or_fail(stream->get_device(), {sycl::aspect::fp16});
        stream->parallel_for(
            sycl::nd_range<3>(sycl::range<3>(1, 1, num_block) * sycl::range<3>(1, 1, 256),
                              sycl::range<3>(1, 1, 256)),
            [=](sycl::nd_item<3> item_ct1) {
                dequantize_int4_to_half(
                    data_in, data_out, scale_buffer, min_val_buffer, num_group, group_size);
            });
    }
}

template <int N>
__dpct_inline__ AlignedArray<sycl::half, N> int8_to_half(const AlignedArray<uint8_t, N>& data)
{
    AlignedArray<sycl::half, N> ret;

#pragma unroll
    for (int idx = 0; idx < N; idx += 1) { ret[idx] = sycl::half(int(data[idx])); }

    return ret;
}

void dequantize_int8_to_half(uint8_t* data_in,
                             sycl::half* data_out,
                             sycl::half* scale_buffer,
                             sycl::half* min_val_buffer,
                             int num_group,
                             int group_size)
{
    auto item_ct1 = sycl::ext::oneapi::experimental::this_nd_item<3>();
    using AccessType = AlignedArray<uint8_t, 8>;
    using AccessTypeOut = AlignedArray<sycl::half, 8>;

    for (int idx = item_ct1.get_local_id(2) + item_ct1.get_group(2) * item_ct1.get_local_range(2);
         idx < num_group * group_size / 8;
         idx += item_ct1.get_local_range(2) * item_ct1.get_group_range(2)) {
        int id_group = idx / (group_size / 8);
        AccessType value = reinterpret_cast<AccessType*>(data_in)[idx];
        sycl::half scale = scale_buffer[id_group];
        sycl::half min_value = min_val_buffer[id_group];

        AccessTypeOut output = int8_to_half(value);
        output = divide<sycl::half, 8>()(output, scale);
        output = plus<sycl::half, 8>()(output, min_value);

        reinterpret_cast<AccessTypeOut*>(data_out)[idx] = output;
    }
}

void launch_dequantize_int8_to_half_experimental(uint8_t* data_in,
                                                 sycl::half* data_out,
                                                 sycl::half* scale_buffer,
                                                 sycl::half* min_val_buffer,
                                                 int num_group,
                                                 int group_size,
                                                 dpct::queue_ptr stream)
{
    int num_warp = num_group / 4;
    int num_block = num_warp / 8;  // 256 trd / block

    {
        dpct::has_capability_or_fail(stream->get_device(), {sycl::aspect::fp16});
        stream->parallel_for(
            sycl::nd_range<3>(sycl::range<3>(1, 1, num_block) * sycl::range<3>(1, 1, 256),
                              sycl::range<3>(1, 1, 256)),
            [=](sycl::nd_item<3> item_ct1) {
                dequantize_int8_to_half(
                    data_in, data_out, scale_buffer, min_val_buffer, num_group, group_size);
            });
    }
}
