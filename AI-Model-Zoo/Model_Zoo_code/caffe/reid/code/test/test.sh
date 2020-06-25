# Copyright 2019 Xilinx Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

export PYTHONPATH=/path_to_caffe_xilinx/caffe_xilinx/python:{PYTHONPATH}
python test.py \
    --prototxt_path /path_to_reid_model/reid/float/test.prototxt \
    --caffemodel_path /path_to_reid_model/reid/float/trainval.caffemodel \
    --dataset_root /path_to_market1501/
