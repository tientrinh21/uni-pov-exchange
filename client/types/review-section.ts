export enum MoodScore {
  VeryBad = 'very bad',
  Bad = 'bad',
  Neutral = 'neutral',
  Good = 'good',
  VeryGood = 'very good',
}

export interface Review {
  review_id: string
  university_id: string
  user_id: string
  title: string
  content: string
  submit_datetime: Date // datetime??
  last_edit_datetime: Date // datetime??
  mood_score: MoodScore
  upvotes: number
  downvotes: number
  has_upvoted: boolean
  has_downvoted: boolean
}
