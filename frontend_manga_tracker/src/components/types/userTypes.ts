export interface UserLogin {
  username: string;
  password: string;
}

export interface UserRegister extends UserLogin {
  email: string;
}

export interface UserApiResponse {
  message: string;
  user?: UserRegister;
  access_token?: string;
}
