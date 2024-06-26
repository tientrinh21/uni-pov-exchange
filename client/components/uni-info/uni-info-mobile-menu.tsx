'use client'

import { Button } from '@/components/ui/button'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'
import { objKeyToText, toRomanNumerals } from '@/lib/utils'
import type { UniversityInfo } from '@/types/university'
import { ArrowUpIcon, DotsHorizontalIcon } from '@radix-ui/react-icons'
import Link from 'next/link'
import { useState } from 'react'
import { ScrollArea } from '@/components/ui/scroll-area'

export default function UniInfoMobileMenu(props: {
  data: UniversityInfo | undefined
}) {
  const [open, setOpen] = useState(false)

  return (
    <DropdownMenu open={open} onOpenChange={setOpen}>
      <DropdownMenuTrigger asChild>
        <div className="sticky top-[4.5rem] z-[200] mx-auto flex w-1/3 justify-center rounded-lg bg-background sm:w-1/4 lg:hidden">
          <Button
            variant="outline"
            className="w-full bg-muted-foreground/15 text-foreground/65"
          >
            <DotsHorizontalIcon className="h-6 w-6 sm:h-8 sm:w-8" />
            <span className="sr-only">Dots Menu</span>
          </Button>
        </div>
      </DropdownMenuTrigger>
      <DropdownMenuContent
        align="center"
        className="md-[80vw] z-[200] rounded-lg px-4 py-4 shadow-xl sm:w-[40vw] lg:hidden"
      >
        <ScrollArea className="h-[300px]">
          {Object.entries(props.data!).map(([key, _], index) => {
            if (key === 'info_page_id') return
            if (key === 'webpage') return
            return (
              <DropdownMenuItem key={index} onClick={() => setOpen(false)}>
                <Link
                  href={`#${key}`}
                  className={`mx-auto my-1 w-full text-base font-medium text-accent-foreground`}
                >
                  <span className="mr-1 inline-block w-8 md:ml-14">{`${toRomanNumerals(index)}.`}</span>
                  <span>{objKeyToText(key)}</span>
                </Link>
              </DropdownMenuItem>
            )
          })}
          <DropdownMenuItem onClick={() => setOpen(false)}>
            <Link
              href=""
              className={`mx-auto my-1 w-full text-base font-medium text-accent-foreground`}
            >
              <ArrowUpIcon className="mr-4 inline-block h-5 w-5 md:ml-14" />
              <span>Back to top</span>
            </Link>
          </DropdownMenuItem>
        </ScrollArea>
      </DropdownMenuContent>
    </DropdownMenu>
  )
}
