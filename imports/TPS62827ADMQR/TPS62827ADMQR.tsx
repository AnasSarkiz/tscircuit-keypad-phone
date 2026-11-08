import objPath from "./TPS62827ADMQR.obj"
import stepPath from "./TPS62827ADMQR.step"
import type { ChipProps } from "@tscircuit/props"

const pinLabels = {
  pin1: ["EN"],
  pin2: ["PG"],
  pin3: ["FB"],
  pin4: ["GND"],
  pin5: ["SW"],
  pin6: ["VIN"]
} as const

const pinAttributes = {
  pin4: {requiresGround: true},
  pin6: {requiresPower: true}
} as const

export const TPS62827ADMQR = (props: ChipProps<typeof pinLabels>) => {
  return (
    <chip
      pinLabels={pinLabels}
      pinAttributes={pinAttributes}
      supplierPartNumbers={{
  "jlcpcb": [
    "C3189972"
  ]
}}
      manufacturerPartNumber="TPS62827ADMQR"
      footprint={<footprint>
        <smtpad portHints={["pin1"]} pcbX="-0.6750558mm" pcbY="0.499999mm" width="0.5999988mm" height="0.2500122mm" shape="rect" />
<smtpad portHints={["pin2"]} pcbX="-0.6750558mm" pcbY="0.000127mm" width="0.5999988mm" height="0.2500122mm" shape="rect" />
<smtpad portHints={["pin3"]} pcbX="-0.6750558mm" pcbY="-0.499999mm" width="0.5999988mm" height="0.2500122mm" shape="rect" />
<smtpad portHints={["pin4"]} pcbX="0.4750562mm" pcbY="-0.499999mm" width="0.999998mm" height="0.2500122mm" shape="rect" />
<smtpad portHints={["pin5"]} pcbX="0.4750562mm" pcbY="0.000127mm" width="0.999998mm" height="0.2500122mm" shape="rect" />
<smtpad portHints={["pin6"]} pcbX="0.4750562mm" pcbY="0.499999mm" width="0.999998mm" height="0.2500122mm" shape="rect" />
<silkscreenpath route={[{"x":-0.7250429999999142,"y":-0.7998714000000291},{"x":0.7749794000000065,"y":-0.7998714000000291}]} />
<silkscreenpath route={[{"x":-0.7250429999999142,"y":0.8001254000000699},{"x":0.7749794000000065,"y":0.8001254000000699}]} />
<silkscreencircle pcbX="-1.2048998mm" pcbY="0.490093mm" radius="0.070104mm" />
<silkscreentext text="{NAME}" pcbX="-0.1401318mm" pcbY="1.787527mm" anchorAlignment="center" fontSize="1mm" />
<courtyardoutline outline={[{"x":-1.2250551999999288,"y":1.0000112000001309},{"x":1.2250552000000425,"y":1.0000112000001309},{"x":1.2250552000000425,"y":-0.9999857999999904},{"x":-1.2250551999999288,"y":-0.9999857999999904},{"x":-1.2250551999999288,"y":1.0000112000001309}]} />
      </footprint>}
      cadModel={{
        objUrl: objPath,
        stepUrl: stepPath,
        pcbRotationOffset: 270,
        modelOriginPosition: { x: 0.000012700000070253736, y: -0.026034999999978936, z: -0.02 },
      }}
      {...props}
    />
  )
}