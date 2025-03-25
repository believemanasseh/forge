export interface Message {
  id: number;
  sender: string;
  text: string;
}

export interface APIResponse {
  status: string;
  message: string;
}
