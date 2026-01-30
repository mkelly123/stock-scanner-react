import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  root: __dirname,     // force Vite to use THIS folder as the root
  publicDir: "public",
  plugins: [react()],
});
