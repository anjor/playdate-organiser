export interface User {
  id: number;
  email: string;
  name: string;
  school_verified: boolean;
  created_at: string;
  updated_at: string;
}

export interface Child {
  id: number;
  name: string;
  year_group: string;
  age: number;
  parent_id: number;
  created_at: string;
}

export interface Playdate {
  id: number;
  title: string;
  description?: string;
  date_time: string;
  location: string;
  child_id: number;
  parent_id: number;
  status: 'active' | 'cancelled' | 'completed';
  created_at: string;
}

export interface Interest {
  id: number;
  playdate_id: number;
  parent_id: number;
  message?: string;
  created_at: string;
}

export interface UserList {
  id: number;
  user_id: number;
  target_user_id: number;
  list_type: 'allowlist' | 'denylist';
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
}