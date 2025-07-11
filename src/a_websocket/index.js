import { io } from "socket.io-client";
import { B_URl } from "../apis/auth";

const socket = io(`${B_URl}/main`, {
    path: "/ws/socket.io",
    transports: ["websocket"],
    withCredentials: true,
});


socket.on("connect", () => {
    console.log("✅ Connected to WebSocket server");

});

socket.on("disconnect", () => {
    console.log("❌ Disconnected from WebSocket server");

});

socket.on("message", (data) => {
    console.log("📩 Received:", data);

});

export default socket;
