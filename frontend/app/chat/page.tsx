import Header from "@/components/Header";
import Disclaimer from "@/components/Disclaimer";
import ChatWindow from "@/components/ChatWindow";

export default function ChatPage() {
  return (
    <div className="flex h-screen flex-col">
      <Header />
      <Disclaimer />
      <div className="flex-1 overflow-hidden bg-gray-50">
        <ChatWindow />
      </div>
    </div>
  );
}
