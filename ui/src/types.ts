export interface Message {
  id: number;
  sender: string;
  text: string;
}

export interface APIResponse {
  status: string;
  message: string;
  data: Data;
}

export interface Data {
  thought: string;
  action: string;
  action_args: ActionArgs;
  result: string;
  response: string;
}

export interface ActionArgs {
  template:
    | "vanilla"
    | "vanilla-ts"
    | "vue"
    | "vue-ts"
    | "react"
    | "react-ts"
    | "react-swc"
    | "react-swc-ts"
    | "preact"
    | "preact-ts"
    | "lit"
    | "lit-ts"
    | "svelte"
    | "svelte-ts"
    | "solid"
    | "solid-ts"
    | "qwik"
    | "qwik-ts";
  project_name: string;
  package_manager: "npx" | "npm" | "yarn" | "pnpm";
}

export interface DownloadDetails {
  projectName: string;
  url: string;
}

export type Theme = "light" | "dark";

export interface ThemeContextType {
  theme: Theme;
  toggleTheme: () => void;
}
