<template>
  <v-container>
    <v-responsive>
      <v-card theme="dark" class="mx-auto pa-10 top-card px-12" rounded="xl"
        style="background-color: rgba(255, 255, 255, 0.233)">
        <v-row class="top-content">
          <v-col>
            <h1 class="text-top text-left">
              Sistem Konversi Citra Panoramik Ke Odontogram
            </h1>
            <div class="font pt-9 text-left" style="
                color: #383838;
                font-size: 30px;
                font-weight: 300;
                line-height: normal;
              ">
              Sistem dengan kemampuan deteksi citra panoramik untuk diubah dalam
              bentuk odontogram lengkap dengan penomoran dan deteksi gigi hilang
            </div>
            <v-btn href="#bottom-section" class="mt-8 text--white" elevation="4" color="#068089" block size="large"
              variant="flat" :class="{ 'button-animation': true }">Coba Deteksi</v-btn>
          </v-col>
          <v-col class="top-right">
            <img src="@/assets/panoramik.png" />
          </v-col>
        </v-row>
      </v-card>
      <div class="mt-2" id="bottom-section"></div>
      <div class="bottom-content" style="min-height: 100vh">
        <v-card class="mx-auto mt-12 pa-7" rounded="xl">
          <v-overlay v-model="overlay" contained class="align-center justify-center text-center" persistent>
            <img src="@/assets/panoramik.png" alt="Preview" class="loading" cover width="150" />

            <h4>Mohon Tunggu Sebenatar..</h4>
          </v-overlay>
          <v-card-text>
            <v-row>
              <v-col my-5>
                <v-form>
                  <v-text-field v-model="nama" label="Nama"></v-text-field>
                  <v-text-field v-model="rekam_medik" label="Nomor Rekam Medik" required></v-text-field>
                  <v-file-input v-model="selectedFile" label="Upload Gambar" accept="image/*" @change="handleFileUpload"
                    clear-icon="false" required></v-file-input>
                  <v-btn :disabled="isFormIncomplete" @click="submitForm" required class="mt-3" color="primary" block
                    size="large">Deteksi Gigi</v-btn>
                </v-form>
              </v-col>
              <v-col>
                <v-img v-if="previewImage" :src="previewImage" alt="Preview" class="image-preview" cover max-height="300">
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
          <v-overlay v-model="overlay" contained class="align-center justify-center text-center" persistent>
            <img src="@/assets/panoramik.png" alt="Preview" class="loading" cover width="150" />

            <h4>Mohon Tunggu Sebenatar..</h4>
          </v-overlay>
          <v-card-text>
            <v-row>
              <v-col>
                <h4>Nama : {{ data.nama }}</h4>
              </v-col>
              <v-col>
                <h4>No Rekam Medik : {{ data.rekam_medik }}</h4>
              </v-col>
              <v-col class="text-right"><v-btn color="red" size="small" variant="flat" @click="deleteData"
                  :disabled="overlay">Hapus</v-btn></v-col>
            </v-row>
            <v-row class="text-center">
              <v-col>
                <img class="text-center" :src="data.gambar" :key="componentKey" />
              </v-col>
            </v-row>
            <v-row class="text-center mt-6">
              <v-col>
                <div class="">
                  <div class="text-center mt-3 d-flex align-center justify-center">
                    <v-expansion-panels style="maxWidth: 1500px">
                      <v-expansion-panel title="Crop Gigi">
                        <v-expansion-panel-text class="py-4">

                          <div class="d-flex mb-6 justify-center align-end">
                            <div v-for="item in odontogramUp" :key="item.number">
                              <v-img v-if="item.isDuplicate == false && item.isMissing == false" class="bg-white mx-1"
                                width="83" max-height="150" :aspect-ratio="1" :src="isSquare?item.urlImageSquare:item.urlImage"></v-img>
                              <div v-if="item.isMissing" style="width:80px" class="mx-1">
                                Hilang
                              </div>
                              <v-card v-if="item.isDuplicate" elevation="1" max-width="444" class="mx-1 ">
                                <v-carousel :continuous="false" :show-arrows="false" hide-delimiter-background
                                   :height="isSquare? 83 : 150">
                                  <v-carousel-item v-for="(item, i) in item.urlImage" :key="i" cover >
                                    <v-img  class="d-flex " width="83" :aspect-ratio="1" :src="item" alt="t"></v-img>
                                  </v-carousel-item>
                                </v-carousel>
                              </v-card>
                              <div class="mt-2">
                                {{ item.number }}
                              </div>
                            </div>
                          </div>
                          <div class="d-flex mt-6 justify-center">
                            <div v-for="item in odontogramDown" :key="item.number">
                              <div class="mb-2">
                                {{ item.number }}
                              </div>
                              <v-img v-if="item.isDuplicate == false && item.isMissing == false" class="bg-white mx-1"
                              width="83" max-height="150" :aspect-ratio="1" :src="isSquare?item.urlImageSquare:item.urlImage"></v-img>
                              <div v-if="item.isMissing" style="width:80px" class="mx-1">
                                Hilang
                              </div>
                              <v-card v-if="item.isDuplicate" elevation="1" max-width="444" class="mx-1">
                                <v-carousel :continuous="false" :show-arrows="false" hide-delimiter-background
                                :height="isSquare? 83 : 150">
                                  <v-carousel-item v-for="(item, i) in item.urlImage" :key="i">
                                    <v-img class="bg-white" width="83" :aspect-ratio="1" :src="item"></v-img>

                                  </v-carousel-item>
                                </v-carousel>
                              </v-card>
                            </div>
                          </div>
                          <div class="d-flex justify-end">
                            <v-btn class="mt-5" size="small" variant="flat" @click="squareCrop">Change to {{isSquare?'Original Crop':'Square crop'}}</v-btn>
                          </div>
                        </v-expansion-panel-text>
                      </v-expansion-panel>
                    </v-expansion-panels>
                  </div>
                </div>
              </v-col>
            </v-row>

            <v-row class="text-center mt-6">
              <v-col class="d-flex justify-center">
                <v-card elevation="3" max-width="1200" class="pa-5 py-10">
                  <h2 class="mb-5">Citra Odontogram</h2>
                  <div class="text-center mt-3">
                    <v-chip v-for="item in odontogramUp" :key="item.number" class="pa-6 ma-1" outlined x-large label
                      :variant="item.isMissing ? 'flat' : undefined">
                      {{ item.number }}
                    </v-chip>
                    <v-chip v-if="odontogramUp.length==0" v-for="(item,k) in customOrderUp" :key="k" class="pa-6 ma-1" outlined x-large label>
                      {{ item }}
                    </v-chip>
                  </div>
                  <div class="text-center mt-12 ">
                    <v-chip v-for="item in odontogramDown" :key="item.number" class="pa-6 ma-1" outlined x-large label
                      :variant="item.isMissing ? 'flat' : undefined">
                      {{ item.number }}
                    </v-chip>
                    <v-chip v-if="odontogramDown.length==0" v-for="(item,k) in customOrderDown" :key="k" class="pa-6 ma-1" outlined x-large label>
                      {{ item }}
                    </v-chip>
                  </div>

                  <div class="text-center mt-3">
                    Keterangan:
                    <div class="d-flex align-center justify-center">
                      <v-chip class="pa-3 ma-1" outlined size="small" label variant="flat">
                      </v-chip>
                      <div>: kotak hitam terindikasi gigi gilang</div>
                    </div>
                  </div>
                </v-card>
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
      odontogramUp: [],
      odontogramDown: [],
      isSquare:false,
      customOrderUp : [
          18, 17, 16, 15, 14, 13, 12, 11, 21, 22, 23, 24, 25, 26, 27, 28,
        ],
        customOrderDown : [
          48, 47, 46, 45, 44, 43, 42, 41, 31, 32, 33, 34, 35, 36, 37, 38,
        ],
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
    squareCrop() {
      this.isSquare = !this.isSquare ;
      this.componentKey++;
    },
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
        this.data = response.data;

        if(this.data.predictions.show_odontogram.length>0){
        this.odontogramUp = this.data.predictions.show_odontogram
          .filter((item) => this.customOrderUp.includes(item.number))
          .sort(
            (a, b) =>
              this.customOrderUp.indexOf(a.number) - this.customOrderUp.indexOf(b.number)
          );
        this.odontogramDown = this.data.predictions.show_odontogram
          .filter((item) => this.customOrderDown.includes(item.number))
          .sort(
            (a, b) =>
              this.customOrderDown.indexOf(a.number) -
              this.customOrderDown.indexOf(b.number)
          );
        }
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
        console.log("Uploading file..." + `${this.apiUrl}/data`);
        await axios.delete(`${this.apiUrl}/data`);
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
      // this.overlay = false;
      window.location.reload();
      this.componentKey++;
    },
    async deleteData() {
      try {
        this.overlay = true;
        await axios.delete(`${this.apiUrl}/data`);
        await this.getAll();
        this.overlay = false;
      } catch (error) {
        console.error(error);
        toast.error("Error : " + error, this.optionToast);
        this.overlay = false;
      }
      window.location.reload();
      // this.componentKey++;
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

.carousel-item-content {
  flex-grow: 1;
  /* This will make the content grow to fill the available space */
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  /* Align content to the bottom of the container */
}
</style>
