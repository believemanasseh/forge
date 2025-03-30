import { useState, useRef, useEffect } from "react";
import send from "./assets/send.png";
import type { MenuProps } from "antd";
import {
  SettingOutlined,
  SunOutlined,
  DownOutlined,
  QuestionOutlined,
  RobotOutlined,
} from "@ant-design/icons";
import { Dropdown, Button, message, Space } from "antd";
import { Squeeze as Hamburger } from "hamburger-react";
import useSWRMutation from "swr/mutation";
import { APIResponse, Message } from "./types";

const chatWithAgent = async (
  url: string,
  {
    arg,
  }: {
    arg: {
      query: string;
      getter: Message[];
      setter: (arg: Message[]) => void;
    };
  }
) => {
  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ query: arg.query }),
  });
  const jsonResponse = (await response.json()) as APIResponse;
  const aiMessage: Message = {
    id: Date.now(),
    sender: "ai",
    text: jsonResponse.message,
  };
  arg.setter([...arg.getter, aiMessage]);
};

const ChatInterface = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isOpen, setOpen] = useState(false);
  const [isMobile, setMobile] = useState(false);
  const chatEndRef = useRef<HTMLDivElement | null>(null);
  const textareaRef = useRef<HTMLTextAreaElement | null>(null);
  const { trigger, isMutating } = useSWRMutation(
    "http://localhost:8000/chat",
    chatWithAgent,
    {
      onError: ({ err }) => {
        message.error(`An error occurred: ${err}`);
      },
    }
  );

  const handleSendMessage = () => {
    if (input.trim()) {
      const newMessage: Message = {
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
      void handleSendMessage();
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
    {
      label: "Help",
      key: "3",
      icon: <QuestionOutlined />,
    },
  ];

  const menuProps = {
    items,
    onClick: handleMenuClick,
  };

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
    const triggerChat = async () => {
      await trigger({
        query: input,
        getter: messages,
        setter: setMessages,
      });
    };
    if (
      messages.length &&
      messages[messages.length - 1].sender === "user" &&
      input
    ) {
      void triggerChat();
    }
  }, [messages, input, trigger]);

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
    <div className="md:grid md:grid-cols-[20%_1fr] h-screen w-screen m-auto overflow-y-auto overflow-x-hidden">
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
      <div className="max-w-[100%] xs:overflow-y-auto xs:overflow-x-hidden">
        <div className="flex flex-col m-auto max-h-[100%] w-[50%]">
          <div className="xs:h-[calc(100vh-100px)] m-auto xs:max-w-[90%] bg-[black] md:max-w-[60%] lg:min-w-[100%] lg:max-w-[100%] rounded-2xl p-5">
            <div className="w-[100%] bg-[blue] m-auto">
              {messages.map((message) => {
                if (message.sender === "ai") {
                  return (
                    <div
                      className="bg-[whitesmoke] rounded-2xl mt-5 p-3 flex flex-row gap-5 max-w-[100%] items-start"
                      key={message.id}
                    >
                      <RobotOutlined
                        className={`${
                          isMutating ? "animate-spin" : ""
                        } mt-1.5 flex-shrink-0`}
                      />
                      <p className="m-auto max-w-[100%] break-words">
                        {message.text}
                      </p>
                    </div>
                  );
                }
                return (
                  <div
                    className="bg-[whitesmoke] rounded-2xl m-[10px_auto] max-w-fit p-3"
                    key={message.id}
                  >
                    <p className="m-auto max-w-[100%] break-words">
                      {message.text}
                    </p>
                  </div>
                );
              })}
              <div ref={chatEndRef} />
            </div>
          </div>
          <div
            className={`transition-all duration-300 ease-in-out m-auto fixed xs:w-[90%] md:w-[60%] lg:w-[50%] xl:w-[40%] ${
              messages.length === 0
                ? "top-[50%] translate-y-[-50%]"
                : "xs:bottom-1 xl:bottom-5"
            } bg-[white] shadow-lg p-5 rounded-2xl`}
          >
            <textarea
              ref={textareaRef}
              className="bg-white m-auto w-[100%] overflow-x-hidden overflow-y-auto border-none outline-none resize-none p-3 rounded-lg"
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
                onClick={() => {
                  void handleSendMessage();
                }}
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;
