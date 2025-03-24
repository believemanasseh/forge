import { useState, useRef, useEffect } from "react";
import send from "./assets/send.png";
import type { MenuProps } from "antd";
import { SettingOutlined, SunOutlined, DownOutlined } from "@ant-design/icons";
import { Dropdown, Button, message, Space } from "antd";
import { Squeeze as Hamburger } from "hamburger-react";

interface Messages {
  id: number;
  sender: string;
  text: string;
}

const ChatInterface = () => {
  const [messages, setMessages] = useState<Messages[]>([]);
  const [input, setInput] = useState("");
  const [isOpen, setOpen] = useState(false);
  const [isMobile, setMobile] = useState(false);
  const chatEndRef = useRef<HTMLDivElement | null>(null);
  const textareaRef = useRef<HTMLTextAreaElement | null>(null);

  const handleSendMessage = () => {
    if (input.trim()) {
      const newMessage = {
        id: Date.now(),
        sender: "user",
        text: input,
      };
      setMessages([...messages, newMessage]);
      setInput("");
      if (textareaRef.current) {
        textareaRef.current.style.height = "50px"; // Reset height after sending
      }
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const handleMenuClick: MenuProps["onClick"] = (e) => {
    message.info("Yo!");
    console.log(e);
  };

  const items: MenuProps["items"] = [
    {
      label: "Toggle theme",
      key: "1",
      icon: <SunOutlined />,
    },
    {
      label: "Settings",
      key: "2",
      icon: <SettingOutlined />,
    },
  ];

  const menuProps = {
    items,
    onClick: handleMenuClick,
  };

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // Manage textarea height
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "50px";
      textareaRef.current.style.height = `${Math.min(
        textareaRef.current.scrollHeight,
        350
      )}px`;
    }
  }, [input]);

  useEffect(() => {
    const handleResize = () => {
      setMobile(window.innerWidth < 768);
      if (window.innerWidth < 768) setOpen(false);
    };

    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  return (
    <div className="md:grid md:grid-cols-[20%_1fr] h-screen w-screen overflow-x-hidden">
      {isMobile ? (
        <div className="m-1">
          <div className={`${isOpen && "absolute top-1 left-1 z-11"}`}>
            <Hamburger toggled={isOpen} toggle={setOpen} hideOutline rounded />
          </div>
          {isOpen && (
            <div className="absolute top-0 left-0 h-screen w-[80%] bg-white shadow-lg z-10">
              <Dropdown
                className="m-5 border-none outline-none text-black hover:text-black text-black"
                menu={menuProps}
                placement="bottomRight"
              >
                <Button className="mt-20 hover:text-black text-black hover:bg-black">
                  <Space className="hover:text-black">
                    Options
                    <DownOutlined />
                  </Space>
                </Button>
              </Dropdown>
            </div>
          )}
        </div>
      ) : (
        <div className="border-r border-r-[#ccc] h-screen">
          <Dropdown
            className="m-5 border-none outline-none text-black hover:text-black text-black"
            menu={menuProps}
            placement="bottomRight"
          >
            <Button className="hover:text-black text-black hover:bg-black">
              <Space className="hover:text-black">
                Options
                <DownOutlined />
              </Space>
            </Button>
          </Dropdown>
        </div>
      )}
      <div className="flex flex-col items-center">
        <div className="overflow-y-auto overflow-x-hidden">
          {messages.map((message) => (
            <div key={message.id} className={`message ${message.sender}`}>
              {message.text}
            </div>
          ))}
          <div ref={chatEndRef} />
        </div>
        <div className="bg-[whitesmoke] p-5 rounded-lg xs:w-[80%] sm:w-[80%] md:w-[60%] lg:w-[50%] xl:w-[40%] m-auto mb-5 fixed bottom-4">
          <textarea
            ref={textareaRef}
            className="min-h-[50px] max-h-[500px] bg-white m-auto w-[100%] overflow-x-hidden overflow-y-auto border-none outline-none resize-none p-3 rounded-lg"
            cols={100}
            placeholder="Type your message..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
          />
          <div className="flex mx-auto justify-end">
            <img
              className="cursor-pointer w-[40px] h-auto"
              src={send}
              alt="send message"
              onClick={handleSendMessage}
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;
