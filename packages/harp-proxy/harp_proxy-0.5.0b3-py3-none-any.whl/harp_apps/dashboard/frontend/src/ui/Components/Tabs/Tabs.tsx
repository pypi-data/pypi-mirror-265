import { Tab as HeadlessTab } from "@headlessui/react"
import { ReactNode } from "react"
import tw, { styled } from "twin.macro"

const SC = {
  List: styled(HeadlessTab.List)(() => [tw`border-b border-primary-900 flex space-x-4 px-4`]),
  InnerTab: styled("span")(({ selected = false }: { selected?: boolean }) => [
    tw`block`,
    tw`font-medium text-base cursor-pointer`,
    tw`rounded-t-sm border border-b-0 border-primary-900 px-3 py-2`,
    selected ? tw`bg-primary-900 border-primary-900 text-white` : tw`text-primary-900`,
  ]),
  Panels: styled(HeadlessTab.Panels)(() => [tw`p-4 border border-t-0 border-primary-900 max-w-full`]),
  Panel: styled(HeadlessTab.Panel)(() => [tw`overflow-auto`]),
}

function CustomHeadlessTab({ children }: { children: ReactNode }) {
  return (
    <HeadlessTab as="button" className="focus:ring-0 focus:ring-offset-0 focus:outline-none">
      {({ selected }) => <SC.InnerTab selected={selected}>{children}</SC.InnerTab>}
    </HeadlessTab>
  )
}

export const Tab = Object.assign(CustomHeadlessTab, {
  Group: HeadlessTab.Group,
  List: SC.List,
  Panels: SC.Panels,
  Panel: SC.Panel,
})
