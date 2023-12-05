// Plugins
import vue from "@vitejs/plugin-vue";
import vuetify, { transformAssetUrls } from "vite-plugin-vuetify";

// Utilities
import { defineConfig,loadEnv } from "vite";
import { fileURLToPath, URL } from "node:url";


// https://vitejs.dev/config/
export default defineConfig(({ command, mode })=>{
  const env = loadEnv(mode, process.cwd(), '')
  return {
  plugins: [
    vue({
      template: { transformAssetUrls },
    }),
    // https://github.com/vuetifyjs/vuetify-loader/tree/next/packages/vite-plugin
    vuetify({
      autoImport: true,
    }),
  ],
  define: {

      'process.env.VUE_APP_API_BASE_URL': JSON.stringify(env.BASE_URL),
      'process.env.PORT': JSON.stringify(env.PORT),

  },
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
    },
    extensions: [".js", ".json", ".jsx", ".mjs", ".ts", ".tsx", ".vue"],
  },
  server: {
    port: env.PORT,
  },
}}
);
