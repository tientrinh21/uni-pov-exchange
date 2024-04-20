import React from 'react'
import Link from 'next/link'
import { toRomanNumerals } from '@/lib/utils'

function UniInfoName(props: { name: string }) {
  return (
    <h2 className="lg:md-6 mb-2 text-xl font-bold text-primary-foreground sm:mb-3 sm:text-2xl md:mb-4 md:text-3xl lg:text-4xl">
      {props.name}
    </h2>
  )
}

function UniInfoMeta(props: { meta: string }) {
  return (
    <span className=" text-xs font-medium leading-5 text-primary-foreground sm:text-sm sm:leading-6 md:text-base md:leading-7">
      {props.meta}
    </span>
  )
}

function UniInfoContainer(props: { children: React.ReactNode }) {
  return (
    <div className="container flex w-full max-w-screen-lg flex-col pb-6 lg:pb-8">
      {props.children}
    </div>
  )
}

function UniInfoImgWrapper(props: {
  children: React.ReactNode
  imgSrc: string
}) {
  return (
    <div
      className="md:80 flex h-48 w-screen items-end justify-center bg-cover bg-center sm:h-72 lg:h-96"
      style={{
        backgroundImage: `linear-gradient(to right, rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), url(${props.imgSrc})`,
      }}
    >
      {props.children}
    </div>
  )
}

function UniInfoContent(props: { data: Object }) {
  return (
    <div className="pb-[1000px] lg:order-1">
      {Object.entries(props.data).map(([key, value], index) => {
        if (key === 'webpage')
          return (
            <div
              key={index}
              className="mb-8 flex w-full items-center justify-center gap-2 font-medium lg:justify-normal"
            >
              <span className="text-primary sm:text-lg">Webpage:</span>{' '}
              <Link
                href={value}
                target="_blank"
                className="text-secondary-foreground underline underline-offset-2 hover:text-muted-foreground"
              >
                {value}
              </Link>
            </div>
          )

        return (
          <div
            key={index}
            id={key}
            className="mt-[-6rem] space-y-5 pb-8 pt-[6rem]"
          >
            <h3 className="text-xl font-bold text-foreground md:text-2xl">
              {`${toRomanNumerals(index)}. ${key[0].toUpperCase()}${key.substring(1)}`}
            </h3>
            <p className="font-medium text-secondary-foreground">{value}</p>
          </div>
        )
      })}
    </div>
  )
}

function UniInfoNav(props: { data: Object }) {
  return (
    <div className="w-[30%] min-w-44 lg:order-2 lg:min-w-52">
      <div className="sticky top-20">
        {Object.entries(props.data).map(([key, _], index) => {
          if (key === 'webpage') return
          return (
            <div
              key={index}
              className="w-full border-b-2 border-y-accent-foreground/30 py-5 first:border-t-2"
            >
              <Link
                href={`#${key}`}
                className="font-medium text-accent-foreground/75 hover:text-foreground"
              >
                <span className="mr-1 inline-block w-8">{`${toRomanNumerals(index)}.`}</span>
                <span>{`${key[0].toUpperCase()}${key.substring(1)}`}</span>
              </Link>
            </div>
          )
        })}
      </div>
    </div>
  )
}

export {
  UniInfoName,
  UniInfoMeta,
  UniInfoContainer,
  UniInfoImgWrapper,
  UniInfoContent,
  UniInfoNav,
}
