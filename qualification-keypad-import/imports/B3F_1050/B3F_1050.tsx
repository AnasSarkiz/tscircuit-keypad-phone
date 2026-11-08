import objPath from "./B3F_1050.obj"
import stepPath from "./B3F_1050.step"
import type { PushButtonProps } from "@tscircuit/props"

const pinLabels = {
  pin1: ["pin1"],
  pin2: ["pin2"],
  pin3: ["pin3"],
  pin4: ["pin4"]
} as const

export const B3F_1050 = (props: PushButtonProps<typeof pinLabels>) => {
  const { name = "SW1", ...restProps } = props

  return (
    <pushbutton
      name={name}
      pinLabels={pinLabels}
      supplierPartNumbers={{
  "jlcpcb": [
    "C93151"
  ]
}}
      manufacturerPartNumber="B3F-1050"
      footprint={<footprint>
        <platedhole  portHints={["pin1"]} pcbX="-3.24993mm" pcbY="2.249932mm" outerDiameter="1.7999964mm" holeDiameter="1.1999976mm" shape="circle" />
<platedhole  portHints={["pin2"]} pcbX="3.24993mm" pcbY="2.249932mm" outerDiameter="1.7999964mm" holeDiameter="1.1999976mm" shape="circle" />
<platedhole  portHints={["pin3"]} pcbX="-3.24993mm" pcbY="-2.249932mm" outerDiameter="1.7999964mm" holeDiameter="1.1999976mm" shape="circle" />
<platedhole  portHints={["pin4"]} pcbX="3.24993mm" pcbY="-2.249932mm" outerDiameter="1.7999964mm" holeDiameter="1.1999976mm" shape="circle" />
<silkscreenpath route={[{"x":-2.4041100000001734,"y":2.999994000000015},{"x":2.4041100000000597,"y":2.999994000000015}]} />
<silkscreenpath route={[{"x":-2.999994000000129,"y":-1.1468099999999595},{"x":-2.999994000000129,"y":1.1468099999999595}]} />
<silkscreenpath route={[{"x":2.4041100000000597,"y":-2.999994000000015},{"x":-2.4041100000001734,"y":-2.999994000000015}]} />
<silkscreenpath route={[{"x":2.999994000000015,"y":1.1468099999999595},{"x":2.999994000000015,"y":-1.1468099999999595}]} />
<silkscreencircle pcbX="0mm" pcbY="0mm" radius="1.5999968mm" />
<silkscreencircle pcbX="1.6999966mm" pcbY="1.6999966mm" radius="0.2999994mm" />
<silkscreencircle pcbX="-1.6999966mm" pcbY="1.6999966mm" radius="0.2999994mm" />
<silkscreencircle pcbX="-1.6999966mm" pcbY="-1.6999966mm" radius="0.2999994mm" />
<silkscreencircle pcbX="1.6999966mm" pcbY="-1.6999966mm" radius="0.2999994mm" />
<silkscreentext text="{NAME}" pcbX="0.0127mm" pcbY="4.2004mm" anchorAlignment="center" fontSize="1mm" />
<courtyardoutline outline={[{"x":-4.399928199999977,"y":3.3999302000000853},{"x":4.399928199999863,"y":3.3999302000000853},{"x":4.399928199999863,"y":-3.3999302000000853},{"x":-4.399928199999977,"y":-3.3999302000000853},{"x":-4.399928199999977,"y":3.3999302000000853}]} />
      </footprint>}
      cadModel={{
        objUrl: objPath,
        stepUrl: stepPath,
        pcbRotationOffset: 90,
        modelOriginPosition: { x: 0, y: 0, z: -0.000006999999999646178 },
      }}
      {...restProps}
    />
  )
}