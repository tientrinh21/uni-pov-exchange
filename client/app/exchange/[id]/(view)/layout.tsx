import {
  UniHeaderContainer,
  UniHeaderImgWrapper,
  UniHeaderMeta,
  UniHeaderName,
} from '@/components/uni-header'
import { fetchUniversity } from '@/lib/request'
import type { University } from '@/types/university'

const BASE_URL = process.env.BASE_URL || 'http://localhost:8080/api'

export default async function ExchangeLayout({
  children,
  params,
}: {
  children: React.ReactNode
  params: { id: string }
}) {
  const data: University = await fetchUniversity(params.id)

  return (
    <div className="flex flex-col gap-4 md:gap-8">
      <UniHeaderImgWrapper imgSrc={`/${data!.university_id}.jpg`}>
        <UniHeaderContainer>
          <UniHeaderName name={data!.long_name} />
          <UniHeaderMeta meta={`${data!.region}`} />
          <UniHeaderMeta meta={data!.country_name} />
          <UniHeaderMeta meta={`QS Ranking #${data!.ranking}`} />
        </UniHeaderContainer>
      </UniHeaderImgWrapper>

      <div className="container flex max-w-screen-lg flex-col items-center gap-6 lg:items-baseline lg:gap-10">
        {children}
      </div>
    </div>
  )
}
