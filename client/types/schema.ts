import { z } from 'zod'

/* UNIVERSITY */
// UNI HEADER
export const uniHeaderFormSchema = z.object({
  long_name: z.string().optional(),
  country_code: z.string().optional(),
  region: z.string().optional(),
  campus: z.string().optional(),
  ranking: z.string().optional(),
  housing: z.string().optional(),
})

export type UniHeaderFormSchema = z.infer<typeof uniHeaderFormSchema>

// UNI INFO
export const uniInfoFormSchema = z.object({
  webpage: z.string().optional(),
  introduction: z.string().optional(),
  location: z.string().optional(),
  semester: z.string().optional(),
  application_deadlines: z.string().optional(),
  courses: z.string().optional(),
  housing: z.string().optional(),
  expenses: z.string().optional(),
  visa: z.string().optional(),
  eligibility: z.string().optional(),
  requirements: z.string().optional(),
  additional_information: z.string().optional(),
})

export type UniInfoFormSchema = z.infer<typeof uniInfoFormSchema>

// REVIEW

export const reviewFormSchema = z.object({
  title: z.string().min(1, 'Title should not be empty'),
  content: z
    .string()
    .min(1, 'Help other students by writing a bit about your experience'),
  mood_score: z.string().min(1, 'How satisfied were you?'),
})

export type ReviewFormSchema = z.infer<typeof reviewFormSchema>

/* USER */
// LOGIN
export const loginFormSchema = z.object({
  username: z
    .string()
    .min(2, { message: 'Username must be 2 or more characters long' })
    .max(50),
  password: z
    .string()
    .min(2, { message: 'Password must be 2 or more characters long' })
    .max(50),
})

export type LoginFormSchema = z.infer<typeof loginFormSchema>

// REGISTER
export const registerFormSchema = z.object({
  username: z
    .string()
    .min(2, { message: 'Username must be 2 or more characters long' })
    .max(50),
  password: z
    .string()
    .min(2, { message: 'Password must be 2 or more characters long' })
    .max(50),
  nationality: z.string().optional(),
  home_university: z.string().optional(),
})

export type RegisterFormSchema = z.infer<typeof registerFormSchema>

// UPDATE PROFILE
export const profileFormSchema = z.object({
  password: z
    .string()
    .min(2, { message: 'Password must be 2 or more characters long' })
    .max(50)
    .optional()
    .or(z.literal('')),
  nationality: z.string().optional(),
  home_university: z.string().optional(),
})

export type ProfileFormSchema = z.infer<typeof profileFormSchema>
