// Data fetching
// https://www.youtube.com/watch?v=00lxm_doFYw

export interface University {
  university_id: string;
  country_code: string;
  region: string;
  long_name: string;
  info_page_id: string;
  ranking: number;
  housing: boolean;
  campus: string
}

export interface UniversityObject {
  code: string;
  name: string;
  campus: string;
  region: string;
  ranking: number;
  dorm: boolean;
}
