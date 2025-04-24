import { memo } from "react";
import { RobotOutlined } from "@ant-design/icons";
import { MessageItemProps } from "../types";

export const MessageItem = memo(
  ({ message, isLastMessage, isMutating }: MessageItemProps) => {
    if (message.sender === "ai") {
      return (
        <div className="flex justify-left items-left">
          <div className="bg-[var(--bg-secondary)] rounded-2xl mt-5 p-3 flex flex-row gap-5 max-w-fit items-start text-[var(--text-primary)]">
            <RobotOutlined
              className={`${
                isLastMessage && isMutating ? "animate-spin" : ""
              } mt-1.5 flex-shrink-0`}
            />
            <p className="m-auto max-w-[100%] break-words text-[var(--text-primary)]">
              {message.text}
            </p>
          </div>
        </div>
      );
    }
    return (
      <div className="flex justify-right items-right">
        <div className="bg-[var(--bg-secondary)] rounded-2xl m-[10px_auto] max-w-fit p-3 text-[var(--text-primary)]">
          <p className="m-auto max-w-[100%] break-words">{message.text}</p>
        </div>
      </div>
    );
  }
);
