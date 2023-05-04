<template>
  <div>
    <div v-if="isTagDisallowed" class="CardContainer">
      <div class="CardType">
        <el-image style="width: 100%; height: 100%" :src="'image?id=' + imageId">
        </el-image>
        <el-row style="margin-top: 10px">
          <el-col :span="4">
            <el-tooltip class="item" effect="dark" :content="isCollectedLoading
                ? 'waiting...'
                : isCollected
                  ? 'Don\'t collect it'
                  : 'Collect it'
              ">
              <div v-if="!isCollectedLoading">
                <em :class="isCollected ? 'el-icon-star-on' : 'el-icon-star-off'" style="font-size: 20px"
                  @click="collectImage"></em>
              </div>
              <div v-else>
                <em class="el-icon-loading" style="font-size: 20px"></em>
              </div>
            </el-tooltip>
          </el-col>
          <el-col :span="4">
            <el-tooltip content="zoom in" effect="light">
              <em class="el-icon-zoom-in" style="font-size: 20px" @click="viewBigImage"></em>
            </el-tooltip>
          </el-col>
          <el-col :span="16">
            <h4 style="text-align: center; margin: 0%">Id: {{ imageId }}</h4>
          </el-col>
        </el-row>
        <div style="margin: 0%">
          <el-tag v-for="(tag, idx) in this.tags" :key="idx" :type="colors[idx]">
            <div style="color: black">{{ tag }}</div>
          </el-tag>
        </div>

        <el-dialog :visible.sync="dialogVisible">
          <img width="100%" height="100%" :src="'image?id=' + imageId" alt="big" />
        </el-dialog>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "ImageCard",

  data() {
    return {
      colors: ["success", "info", "warning", "danger"],
      imageSource: "",
      isMouseOn: false,
      tags: [],
      isCollected: false,
      dialogVisible: false,
      isCollectedLoading: false,
    };
  },

  computed: {
    isTagDisallowed() {
      if (!this.hideTags) {
        return true;
      }
      for (let i = 0; i < this.tags.length; i++) {
        if (this.disallowedTags.indexOf(this.tags[i]) != -1) {
          return false;
        }
      }
      return true;
    },
  },

  props: {
    imageUrl: String,
    imageId: String,
    disallowedTags: Array,
    hideTags: Boolean,
  },

  created() {
    // 获取图片详细信息
    axios({
      method: "get",
      url: "info",
      params: {
        id: this.imageId,
      },
    })
      .then((res) => {
        this.isCollected = res.data.isCollected;
        this.tags = res.data.tags;
      })
  },

  methods: {
    collectImage() {
      this.isCollectedLoading = true;
      axios({
        method: "get",
        url: "collect",
        params: {
          id: this.imageId,
        },
      })
        .then(() => {
          setTimeout(() => {
            this.isCollected = !this.isCollected;
            if (this.isCollected) {
              this.$message({
                message: 'Collected successfully',
                type: 'success'
              });
            } else {
              this.$message({
                message: 'Removed successfully!',
                type: 'success'
              });
            }
            this.isCollectedLoading = false;
          }, 600);
        })
        .finally(() => {
          this.$emit("changeCollect");
          this.isCollectedLoading = false;
        });
    },
    viewBigImage() {
      this.dialogVisible = true;
    },
  },
};
</script>

<style>
.CardType {
  width: 95%;
  height: 95%;
  margin: 2 auto;
  margin-top: 5px;
  background-color: rgb(173, 238, 239);
  cursor: pointer;
}
</style>

<style scoped>
.el-divider--vertical {
  height: 4em !important;
  width: 1.5px !important;
}

.icon-love {
  position: absolute;
  left: 40%;
  bottom: 40%;
}

/* 标签列表 */
.label-list {
  padding: 1px 1px;
  margin: 1px 1px;
}

.el-tag {
  float: left;
  white-space: pre-line;
  word-break: break-all;
  margin-top: 5px;
  margin-left: 5px;
  max-height: 4vh;
  color: white;
}

.CardContainer {
  width: 270px;
  height: 290px;
  margin-bottom: 20px;
  margin-left: 25px;
}
</style>
