import { type LoginFormSchema, type RegisterFormSchema } from '@/types/schema'
import { type University } from '@/types/university'
import { type User } from '@/types/user'
import axios from 'axios'
import countries from './countries.json'

const BASE_URL = process.env.BASE_URL || 'http://localhost:8080/api'

export async function fetchUniversities() {
  return axios.get<University[]>(`${BASE_URL}/universities`).then((r) => r.data)
}

export async function fetchUser({ username, password }: LoginFormSchema) {
  return axios
    .get<User>(`${BASE_URL}/users/login`, {
      params: {
        username: username,
        pwd: password,
      },
    })
    .then((r) => r.data)
}

export async function createUser({
  username,
  password,
  nationality,
  home_university,
}: RegisterFormSchema) {
  return axios
    .post<User>(`${BASE_URL}/users`, null, {
      params: {
        username: username,
        pwd: password,
        nationality: nationality,
        home_university: home_university,
      },
    })
    .then((r) => r.data)
}

export async function updateUser(
  user: User,
  { password, nationality, home_university }: RegisterFormSchema,
) {
  return axios
    .patch<User>(`${BASE_URL}/users`, null, {
      params: {
        user_id: user.user_id,
        pwd: password,
        nationality: nationality,
        home_university: home_university,
      },
    })
    .then((r) => r.data)
}

export async function deleteUser(user: User) {
  return axios
    .delete(`${BASE_URL}/users`, {
      params: {
        user_id: user.user_id,
      },
    })
    .then((r) => r.data)
}
