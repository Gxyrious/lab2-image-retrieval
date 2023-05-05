<template>
  <div class="container">
    <div style="margin-top: 1%;">
      <el-row>
        <el-col :span="3">
          <el-row>
            <p>please upload your image</p>
          </el-row>
          <el-row type="flex" justify="center" align="middle">
            <el-button
              :icon="isSearchLoading ? 'el-icon-loading' : 'el-icon-search'" type="primary"
              :disabled="fileList.length == 0 || isSearchLoading" @click="search">搜索
            </el-button>
            <el-button
              @click="openCollection" type="warning" @changeCollect="getCollection"
              :disabled="collectDialogVisible">我的收藏
            </el-button>
          </el-row>

        </el-col>
        <el-col :span="3">
          <image-uploader class="image-upload" v-bind:fileList="fileList" ref="uploadImage" @success="uploadSuccess" />
        </el-col>

        <el-col :span="18">
          <template v-if="responseImage.length != 0">
            <p>label filter:</p>
            <div class="label-list">
              <div v-for="(item, idx) in tags" :key="idx">
                <el-tag :hit="false" :type="item.color">
                  <el-checkbox v-model="item.status" @change="tagToggle" />
                  {{ item.label }}
                </el-tag>
              </div>
            </div>
          </template>
        </el-col>
      </el-row>
    </div>

    <div v-if="responseImage.length != 0">
      <el-divider>find {{ this.responseImage.length }} similar images</el-divider>
      <div style="width: 90%;margin:0 auto" class="flex-container">
        <div v-for="(item, idx) in responseImage" :key="idx">
          <ImageCard :imageUrl="item" :disallowedTags="disallowedTags" :hideTags="true" :imageId="item" />
        </div>
      </div>
    </div>

    <el-dialog title="Collection" :visible.sync="collectDialogVisible" :close-on-click-modal="false"
      :modal-append-to-body="false" width="65%">
      <div v-loading="isFavouriteLoading">
        <div style="margin:0 auto" class="flex-container">
          <div v-for="(item, index) in collectImage.slice((currentPage - 1) * 3, currentPage * 3)" :key="index">
            <ImageCard :imageUrl="item" :disallowedTags="disallowedTags" :hideTags="false" :imageId="item" />
          </div>
        </div>
      </div>
      <el-pagination background layout="prev, pager, next" :hide-on-single-page="true" :page-size="3"
        @current-change="handleCurrentChange" :total="collectImage.length">
      </el-pagination>

    </el-dialog>

  </div>
</template>

<script>
import ImageUploader from '@/components/ImageUploader.vue';
import ImageCard from '@/components/ImageCard.vue';
import axios from 'axios';

export default {
  name: 'Home',
  components: {
    ImageUploader,
    ImageCard,
  },
  data() {
    return {
      fileList: [],
      responseImage: [],
      filterImage: [],
      tags: [],
      disallowedTags: [],
      collectImage: [],
      collectDialogVisible: false,
      currentPage: 1,
      isSearchLoading: false,
      isFavouriteLoading: false,
    }
  },
  created() {
    axios({
      method: 'get',
      url: 'tags',
    }).then(res => {
      const colors = ["success", "info", "warning", "danger"];
      this.tags = res.data.map((item) => {
        item.color = colors[Math.floor(Math.random() * (colors.length))];
        item.status = true;
        return item;
      });
      this.disallowedTags = [];
    }).catch(() => {
      const colors = ["success", "info", "warning", "danger"];
      let tmp_res_data = [{ 'label': 'people', 'size': 1220 }, { 'label': 'structures', 'size': 1095 }, { 'label': 'plant_life', 'size': 1019 }, { 'label': 'indoor', 'size': 893 }, { 'label': 'female', 'size': 706 }, { 'label': 'male', 'size': 694 }, { 'label': 'clouds', 'size': 486 }, { 'label': 'portrait', 'size': 484 }, { 'label': 'tree', 'size': 473 }, { 'label': 'animals', 'size': 375 }, { 'label': 'water', 'size': 375 }, { 'label': 'night', 'size': 312 }, { 'label': 'flower', 'size': 297 }, { 'label': 'transport', 'size': 293 }, { 'label': 'sunset', 'size': 292 }, { 'label': 'sea', 'size': 129 }, { 'label': 'car', 'size': 125 }, { 'label': 'food', 'size': 102 }, { 'label': 'bird', 'size': 84 }, { 'label': 'dog', 'size': 82 }, { 'label': 'river', 'size': 56 }, { 'label': 'lake', 'size': 37 }, { 'label': 'baby', 'size': 35 }]
      this.tags = tmp_res_data.map((item) => {
        item.color = colors[Math.floor(Math.random() * (colors.length))];
        item.status = true;
        return item;
      });
      this.disallowedTags = [];
    })

  },
  methods: {
    uploadSuccess(res) {
      this.responseImage = res;
      this.isSearchLoading = false;
    },
    search() {
      this.isSearchLoading = true;
      this.$refs.uploadImage.submitUpload();
    },
    tagToggle() {
      let disallowedTags = [];
      this.tags.forEach(item => {
        if (!item.status) {
          disallowedTags.push(item.label);
        }
      });
      this.disallowedTags = disallowedTags;
    },
    openCollection() {
      this.getCollection();
      this.collectDialogVisible = true;
    },
    handleCurrentChange(val) {
      this.currentPage = val;
    },
    getCollection() {
      this.isFavouriteLoading = true;
      axios({
        method: 'get',
        url: 'collect/all',
      }).then(response => {
        this.collectImage = response.data;
      }).catch(() => {

      }).finally(() => {
        this.isFavouriteLoading = false;
      })
    }
  },
}
</script>

<style scoped>
.flex-container {
  display: flex;
  flex-direction: row;
  /*容器内成员的排列方式为从左到右*/
  flex-wrap: wrap;
  /*换行方式，放不下就换行*/
  justify-content: flex-start;
  /*项目在主轴上的对齐方式*/
  align-content: flex-start;
}



.el-divider--vertical {
  height: 60em !important;
  width: 1.5px !important;
}

.el-tag {
  float: left;
  white-space: pre-line;
  word-break: break-all;
  margin-top: 5px;
  margin-left: 5px;

}
</style>