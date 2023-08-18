<template>
  <v-container>
    <v-responsive>
      <v-card
        theme="dark"
        class="mx-auto pa-10 top-card px-12"
        rounded="xl"
        style="background-color: rgba(255, 255, 255, 0.233)"
      >
        <v-row class="top-content">
          <v-col>
            <h1 class="text-top text-left">
              Sistem Konversi Citra Panoramik Ke Odontogram
            </h1>
            <div
              class="font pt-9 text-left"
              style="
                color: #383838;
                font-size: 30px;
                font-weight: 300;
                line-height: normal;
              "
            >
              Sistem dengan kemampuan deteksi citra panoramik untuk diubah dalam
              bentuk odontogram lengkap dengan penomoran dan deteksi gigi hilang
            </div>
            <v-btn
              href="#bottom-section"
              class="mt-8 text--white"
              elevation="4"
              color="#068089"
              block
              size="large"
              variant="flat"
              :class="{ 'button-animation': true }"
              >Coba Deteksi</v-btn
            >
          </v-col>
          <v-col class="top-right">
            <img src="@/assets/panoramik.png" />
          </v-col>
        </v-row>
      </v-card>
      <div class="mt-2" id="bottom-section"></div>
      <div class="bottom-content" style="min-height: 100vh">
        <v-card class="mx-auto mt-12 pa-7" rounded="xl">
          <v-overlay
            v-model="overlay"
            contained
            class="align-center justify-center text-center"
            persistent
          >
            <img
              src="@/assets/panoramik.png"
              alt="Preview"
              class="loading"
              cover
              width="150"
            />

            <h4>Mohon Tunggu Sebenatar..</h4>
          </v-overlay>
          <v-card-text>
            <v-row>
              <v-col my-5>
                <v-form @submit="submitForm">
                  <v-text-field v-model="nama" label="Nama"></v-text-field>
                  <v-text-field
                    v-model="rekam_medik"
                    label="Nomor Rekam Medik"
                    required
                  ></v-text-field>
                  <v-file-input
                    v-model="selectedFile"
                    label="Upload Gambar"
                    accept="image/*"
                    @change="handleFileUpload"
                    clear-icon="false"
                    required
                  ></v-file-input>
                  <v-btn
                    :disabled="isFormIncomplete"
                    required
                    class="mt-3"
                    type="submit"
                    color="primary"
                    block
                    size="large"
                    >Deteksi Gigi</v-btn
                  >
                </v-form>
              </v-col>
              <v-col>
                <v-img
                  v-if="previewImage"
                  :src="previewImage"
                  alt="Preview"
                  class="image-preview"
                  cover
                  max-height="300"
                >
                  <div class="image-overlay">
                    <span class="image-text"></span>
                  </div>
                </v-img>
                <div v-else class="no-image">No Image</div>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>

        <v-card class="mx-auto mt-1 pa-7" rounded="xl">
          <v-card-text>
            <v-row>
              <v-col
                ><h4>Nama : {{ data.nama }}</h4></v-col
              >
              <v-col
                ><h4>No Rekam Medik : {{ data.rekam_medik }}</h4></v-col
              >
              <v-col class="text-right"
                ><v-btn
                  color="red"
                  size="small"
                  variant="flat"
                  @click="deleteData"
                  :disabled="overlay"
                  >Hapus</v-btn
                ></v-col
              >
            </v-row>
            <v-row class="text-center">
              <v-col>
                <img
                  class="text-center"
                  :src="data.gambar"
                  :key="componentKey"
                />
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </div>
    </v-responsive>
  </v-container>
</template>

<script>
import axios from "axios";
import { toast } from "vue3-toastify";
import "vue3-toastify/dist/index.css";

export default {
  data() {
    return {
      apiUrl: process.env.VUE_APP_API_BASE_URL,
      nama: "",
      rekam_medik: "",
      selectedFile: null,
      previewImage: null,
      data: {},
      overlay: false,
      optionToast: {
        transition: "MyCustomTransition",
        theme: "colored",
      },
      componentKey: 0,
    };
  },
  computed: {
    isFormIncomplete() {
      return !this.nama || !this.rekam_medik || !this.selectedFile;
    },
  },
  mounted() {
    this.getAll();
  },

  methods: {
    handleFileUpload() {
      this.previewImage = null;
      const file =
        this.selectedFile instanceof File
          ? this.selectedFile
          : this.selectedFile[0];
      const reader = new FileReader();

      reader.onload = () => {
        this.previewImage = reader.result;
      };

      if (file) {
        reader.readAsDataURL(file);
      }
    },
    async getAll() {
      try {
        const response = await axios.get(`${this.apiUrl}/data`);
        // await axios.get(`${this.apiUrl}/gambar/img.jpg`);
        this.data = response.data;
      } catch (error) {
        console.error(error);
        toast.error("Error : " + error, this.optionToast);
      }
      this.componentKey++;
    },
    async submitForm() {
      let formData = new FormData();
      formData.append("nama", this.nama);
      formData.append("rekam_medik", this.rekam_medik);
      formData.append("file_gambar", this.selectedFile[0]);
      this.overlay = true;

      try {
        const response = await axios.post(`${this.apiUrl}/data`, formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        });
        console.log(response.data);
        // Reset form fields and preview
        this.nama = "";
        this.rekam_medik = "";
        this.selectedFile = null;
        this.previewImage = null;
        toast.success("Berhasil Deteksi Panoramik", this.optionToast);
        this.getAll();
      } catch (error) {
        toast.error("Error : " + error, this.optionToast);
        console.error("Error : " + error);
      }
      this.overlay = false;
      window.location.reload();
    },
    async deleteData() {
      try {
        const response = await axios.delete(`${this.apiUrl}/data`);
        this.getAll();
      } catch (error) {
        console.error(error);
        toast.error("Error : " + error, this.optionToast);
      }
    },
  },
};
</script>
<style>
.top-card {
  height: calc(100vh - 40px);
}
.top-content {
  display: flex !important;
  align-items: center;
  height: 100%;
}
.text-top {
  -webkit-text-stroke: 2px #ffffff;
  color: #058089;
  font-family: "Open Sans-ExtraBold", Helvetica;
  font-size: 50px;
  font-weight: 800;
  letter-spacing: 0;
  line-height: normal;
}
.top-right {
  display: flex;
  justify-content: right;
}
.image-container {
  position: relative;
}

.image-preview {
  position: relative;
  background-size: cover;
}

.image-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  border: 2px dashed #ccc;
}

.image-text {
  font-weight: bold;
  font-size: 24px;
}
.no-image {
  display: flex;
  justify-content: center;
  align-items: center;
  border: 2px dashed #ccc;
  height: 300px;
}

@keyframes buttonAnimation {
  0% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
  100% {
    transform: translateY(0);
  }
}

.button-animation {
  animation: buttonAnimation 2s infinite;
}

@keyframes loadingAnimation {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(0.5);
  }
  100% {
    transform: scale(1);
  }
}

.loading {
  animation: loadingAnimation 1.5s infinite;
}
</style>
