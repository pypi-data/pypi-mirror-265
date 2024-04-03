// Copyright (c) Meta Platforms, Inc. and affiliates.
// All rights reserved.
//
// This source code is licensed under the BSD-style license found in the
// LICENSE file in the root directory of this source tree.

#pragma once

#include <cstdint>
#include <optional>

namespace fairseq2n {

constexpr std::int32_t version_major = 0;
constexpr std::int32_t version_minor = 2;
constexpr std::int32_t version_patch = 1;

constexpr std::optional<std::int32_t> cuda_version_major = std::nullopt;
constexpr std::optional<std::int32_t> cuda_version_minor = std::nullopt;

constexpr bool supports_cuda = cuda_version_major.has_value();

}  // namespace fairseq2n
