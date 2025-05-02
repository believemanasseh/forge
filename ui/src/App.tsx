import { useState, useRef, useEffect, useCallback, lazy } from "react";
import type { MenuProps } from "antd";
import {
  SettingOutlined,
  SunOutlined,
  DownOutlined,
  QuestionOutlined,
  MoonOutlined,
} from "@ant-design/icons";

import { Dropdown, Button, message } from "antd";
import { Squeeze as Hamburger } from "hamburger-react";
import useSWRMutation from "swr/mutation";
import { APIResponse, Message, DownloadDetails } from "./types";
import { useTheme } from "./hooks";
import send from "./assets/send.png";

const MessageItem = lazy(() => import("./components/MessageItem"));

const chatWithAgent = async (
  url: string,
  {
    arg,
  }: {
    arg: {
      query: string;
      getter: Message[];
      setter: (arg: Message[]) => void;
      downloadDetails: DownloadDetails;
      setDownloadDetails: (arg: DownloadDetails) => void;
      setCanTrigger: (arg: boolean) => void;
    };
  }
) => {
  try {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ query: arg.query }),
    });
    const jsonResponse = (await response.json()) as APIResponse;

    if (jsonResponse.data) {
      arg.setDownloadDetails({
        projectName: jsonResponse.data.action_args.project_name,
        url: jsonResponse.data.result,
      });
    }

    const messages = [...arg.getter];
    messages[messages.length - 1] = {
      ...messages[messages.length - 1],
      id: Date.now(),
      text: jsonResponse.message,
    };
    arg.setter(messages);
    arg.setCanTrigger(false);
  } catch (err) {
    message.error(`An error occurred: ${err as Error}`);
  }
};

const ChatInterface = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isOpen, setOpen] = useState(false);
  const [isMobile, setMobile] = useState(false);
  const [canTrigger, setCanTrigger] = useState(false);
  const [downloadDetails, setDownloadDetails] = useState<DownloadDetails>({
    projectName: "",
    url: "",
  });
  const chatEndRef = useRef<HTMLDivElement | null>(null);
  const textareaRef = useRef<HTMLTextAreaElement | null>(null);
  const { trigger, isMutating } = useSWRMutation(
    `${import.meta.env.VITE_API_URL}/chat`,
    chatWithAgent,
    {
      onError: ({ err }) => {
        message.error(`An error occurred: ${err}`);
      },
    }
  );
  const { theme, toggleTheme } = useTheme();

  const handleSendMessage = useCallback(() => {
    if (input.trim()) {
      const newMessages: Message[] = [
        {
          id: Date.now(),
          sender: "user",
          text: input,
        },
        { id: Date.now(), sender: "ai", text: "" },
      ];
      setMessages((prev) => [...prev, ...newMessages]);
      setInput("");
      if (textareaRef.current) {
        textareaRef.current.style.height = "50px"; // Reset height after sending
      }
    }
  }, [input]);

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      setCanTrigger(true);
      void handleSendMessage();
    }
  };

  const handleImageClick = (e: React.MouseEvent<HTMLImageElement>) => {
    e.preventDefault();
    setCanTrigger(true);
    void handleSendMessage();
  };

  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    e.preventDefault();
    setInput(e.target.value);
  };

  const handleButtonClick = (e: React.MouseEvent<HTMLButtonElement>) => {
    e.preventDefault();
    if (downloadDetails.url) {
      void handleDownload(downloadDetails.url);
    }
  };

  const items: MenuProps["items"] = [
    {
      label: "Toggle theme",
      key: "1",
      icon: theme === "light" ? <MoonOutlined /> : <SunOutlined />,
      onClick: () => {
        toggleTheme();
        message.info(
          `Switched to ${theme === "light" ? "dark" : "light"} theme`
        );
      },
      style: {
        color: "var(--text-primary)",
      },
    },
    {
      label: "Settings",
      key: "2",
      icon: <SettingOutlined />,
      style: {
        color: "var(--text-primary)",
      },
    },
    {
      label: "Help",
      key: "3",
      icon: <QuestionOutlined />,
      style: {
        color: "var(--text-primary)",
      },
    },
  ];

  const handleDownload = async (downloadUrl: string) => {
    try {
      const response = await fetch(downloadUrl);
      if (!response.ok) throw new Error("Download failed");

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `${downloadDetails.projectName}.zip`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (error) {
      message.error(`Download failed: ${error as Error}`);
    }
  };

  const menuProps = { items };

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });

    const triggerChat = async () => {
      await trigger({
        query: messages[messages.length - 2].text,
        getter: messages,
        setter: setMessages,
        downloadDetails: downloadDetails,
        setDownloadDetails: setDownloadDetails,
        setCanTrigger: setCanTrigger,
      });
    };

    if (messages.length && canTrigger) {
      void triggerChat();
    }
  }, [messages, downloadDetails, trigger, canTrigger]);

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
    const checkMobile = () => {
      setMobile(window.innerWidth < 768);
      if (window.innerWidth < 768) setOpen(false);
    };

    checkMobile();
    window.addEventListener("resize", checkMobile);
    return () => window.removeEventListener("resize", checkMobile);
  }, [isMobile]);

  return (
    <div className="md:grid md:grid-cols-[20%_1fr] h-screen w-screen m-auto overflow-y-auto overflow-x-hidden bg-[var(--bg-primary)]">
      {isMobile ? (
        <div className="m-1">
          <div className={`${isOpen && "absolute top-1 left-1 z-11"}`}>
            <Hamburger toggled={isOpen} toggle={setOpen} hideOutline rounded />
          </div>
          {isOpen && (
            <div
              className={`absolute top-0 left-0 h-screen w-[80%] shadow-lg z-10 text-center bg-[var(--bg-primary)]`}
            >
              <Dropdown
                className="m-5 border-none outline-none text-[var(--primary)] bg-[var(--primary)]"
                menu={{
                  ...menuProps,
                  style: {
                    backgroundColor: "var(--bg-primary)",
                  },
                }}
                placement="bottomRight"
              >
                <Button
                  className="mt-20"
                  style={{
                    backgroundColor: "var(--bg-primary)",
                    color: "var(--text-primary)",
                    borderColor: "var(--text-primary)",
                  }}
                >
                  Options
                  <DownOutlined />
                </Button>
              </Dropdown>
              {downloadDetails.url && (
                <div className="mt-10 border-t border-t-[#ccc] pt-5">
                  <p>Your project "{downloadDetails.projectName}" is ready!</p>
                  <Button
                    className="mt-5"
                    onClick={handleButtonClick}
                    style={{
                      backgroundColor: "var(--bg-primary)",
                      color: "var(--text-primary)",
                      borderColor: "var(--text-primary)",
                    }}
                  >
                    Download
                  </Button>
                </div>
              )}
            </div>
          )}
        </div>
      ) : (
        <div className="border-r border-r-[#ccc] h-screen text-center">
          <Dropdown
            className="m-5 border-none outline-none bg-[var(--bg-primary)]"
            menu={{
              ...menuProps,
              style: {
                backgroundColor: "var(--bg-primary)",
                color: "white",
              },
            }}
            placement="bottomRight"
          >
            <Button
              style={{
                backgroundColor: "var(--bg-primary)",
                color: "var(--text-primary)",
                borderColor: "var(--text-primary)",
              }}
            >
              Options
              <DownOutlined />
            </Button>
          </Dropdown>
          {downloadDetails.url && (
            <div className="mt-10 border-t border-t-[#ccc] pt-5">
              <p>Your project "{downloadDetails.projectName}" is ready!</p>
              <Button
                className="mt-5"
                onClick={handleButtonClick}
                style={{
                  backgroundColor: "var(--bg-primary)",
                  color: "var(--text-primary)",
                  borderColor: "var(--text-primary)",
                }}
              >
                Download
              </Button>
            </div>
          )}
        </div>
      )}
      <div className="max-w-[100%] xs:overflow-y-auto xs:overflow-x-hidden">
        <div className="flex flex-col m-auto max-h-[100%] xs:w-[100%] sm:w-[50%]">
          <div className="xs:h-[calc(100vh-100px)] m-auto xs:w-[90%] md:w-[100%] rounded-2xl p-5">
            <div className="w-[100%] m-auto">
              {messages.map((message, index) => (
                <MessageItem
                  key={index}
                  message={message}
                  isLastMessage={index === messages.length - 1}
                  isMutating={isMutating}
                />
              ))}
              <div ref={chatEndRef} />
            </div>
          </div>
          <div
            className={`transition-all duration-300 ease-in-out m-[auto_auto_30px_auto] fixed xs:w-[100%] sm:w-[50%] md:w-[45%] lg:w-[50%] xl:w-[40%] ${
              messages.length === 0
                ? "top-[50%] translate-y-[-50%]"
                : "xs:bottom-1 xl:bottom-5"
            } bg-[--var(--bg-primary)] shadow-lg p-5 rounded-2xl border ${
              theme === "light" ? "border-none" : "border-white"
            }`}
          >
            <textarea
              ref={textareaRef}
              className="text-[var(--text-primary)] m-auto w-[100%] overflow-x-hidden overflow-y-auto outline-none resize-none p-3 rounded-lg"
              cols={100}
              placeholder="Type your message..."
              value={input}
              onChange={handleChange}
              onKeyDown={handleKeyDown}
            />
            <div className="flex mx-auto justify-end">
              <img
                className="cursor-pointer w-[40px] h-auto bg-white rounded-full"
                src={send}
                alt="send message"
                onClick={handleImageClick}
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;
