export interface User {
  id: number;
  username: string;
  first_name: string;
  last_name: string;
  email: string;
  is_active: boolean;
}

export interface Account {
  id: number;
  user: User;
  profile_image: string | null;
  bio: string;
  created: string;
  qr_code: string | null;
}

export interface Post {
  id: number;
  title: string;
  image: string | null;
  descriptions: string;
  created_at: string;
  account: Account;
  private?: PrivateGroup;
  likes: PostLike[];
  comments: Comment[];
}

export interface PostLike {
  id: number;
  post: number;
  account: number;
}

export interface Comment {
  id: number;
  post: number;
  account: Account;
  content: string;
}

export interface MarketProduct {
  id: number;
  seller: Account;
  product_name: string;
  product_image: string;
  product_price: number;
  product_informations: string;
}

export interface PrivateGroup {
  id: number;
  owner: Account;
  members: Account[];
  code: string;
  created_at: string;
}

export interface PublicGroup {
  id: number;
  owner: Account;
  members: Account[];
  created_at: string;
}

export interface FriendRequest {
  id: number;
  sender: Account;
  receiver: Account;
  status: 'pending' | 'accept' | 'decline';
}

export interface ProfileRate {
  id: number;
  rater: Account;
  profile: Account;
  rate_value: number;
}

export interface Notification {
  id: number;
  account: Account[];
  created_at: string;
  message: string;
  mark_as_read: boolean;
}

export interface Message {
  id: number;
  message_sender: Account;
  message_receiver: Account;
  content: string;
  timestamp: string;
}

export interface AuthResponse {
  access: string;
  refresh: string;
  user: User;
}

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface RegisterData {
  username: string;
  email: string;
  password: string;
  first_name?: string;
  last_name?: string;
} 