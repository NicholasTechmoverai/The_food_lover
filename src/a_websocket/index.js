// a_websocket/index.js
import { io } from "socket.io-client";
import { B_URl } from "../apis/auth";

export const mainSocket = io(`${B_URl}/main`, {
  path: "/ws/socket.io",
  transports: ["websocket"],
  withCredentials: true,
});

export const recipesSocket = io(`${B_URl}/recipes`, {
  path: "/ws/socket.io",
  transports: ["websocket"],
  withCredentials: true,
});

export const usersSocket = io(`${B_URl}/users`, {
  path: "/ws/socket.io",
  transports: ["websocket"],
  withCredentials: true,
});

export const notificationsSocket = io(`${B_URl}/notifications`, {
  path: "/ws/socket.io",
  transports: ["websocket"],
  withCredentials: true,
});

mainSocket.on("connect", () => {
  console.log("✅ Connected to WebSocket server");
});

mainSocket.on("disconnect", () => {
  console.log("❌ Disconnected from WebSocket server");
});

mainSocket.on("message", (data) => {
  console.log("📩 Received:", data);
});
