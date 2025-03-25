import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), tailwindcss()],
  optimizeDeps: {
    include: ["swr"],
  },
  server: {
    allowedHosts: ["localhost", "ebbc-160-152-124-55.ngrok-free.app"],
  },
});
