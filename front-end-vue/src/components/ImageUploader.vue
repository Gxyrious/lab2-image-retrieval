<template>
    <div class="container">
        <el-upload :class="fileList.length == 1 ? 'more' : 'one'" :limit="1" :multiple="false" action="imgUpload"
            :auto-upload="false" :file-list="fileList" list-type="picture-card" :on-change="handleChange"
            :on-success="handleSuccess" ref="uploadRef"
            >
            <em slot="default" class="el-icon-plus"></em>
            <div slot="file" slot-scope="{file}">
                <img class="el-upload-list__item-thumbnail" :src="file.url" alt="image">
                <span class="el-upload-list__item-actions">
                    <span class="el-upload-list__item-preview" @click="showImgDiag(file)">
                        <em class="el-icon-zoom-in"></em>
                    </span>
                    <span class="el-upload-list__item-delete" @click="delImg(file)">
                        <em class="el-icon-delete"></em>
                    </span>
                </span>
            </div>
        </el-upload>
        <el-dialog :visible.sync="isDiagVisible">
            <img width="80%" height="80%" :src="diagImgUrl" alt="big-image">
        </el-dialog>
    </div>
</template>
<script>
export default {
    data() {
        return {
            diagImgUrl: '',
            isDiagVisible: false,
        };
    },
    props: {
        fileList: [],
    },
    methods: {
        showImgDiag(file) {
            this.diagImgUrl = file.url;
            this.isDiagVisible = true;
        },
        delImg() {
            this.fileList.splice(0, 1);
        },
        handleChange(file) {
            if (this.fileList.length != 1) {
                this.fileList.push(file);
            }
        },
        handleSuccess(res) {
            this.$emit('success', res);
        },
        submitUpload() {
            this.$refs.uploadRef.submit();
        },
    }
}
</script>



<style scoped>
::v-deep .more .el-upload--picture-card {
    display: none;
}
::v-deep .el-upload-list__item {
    transition: none !important;
  }
</style>