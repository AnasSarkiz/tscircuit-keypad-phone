import objPath from "./TPD6S300ARUKR.obj"
import stepPath from "./TPD6S300ARUKR.step"
import type { ChipProps } from "@tscircuit/props"

const pinLabels = {
  pin1: ["C_SUB1"],
  pin2: ["C_SUB2"],
  pin3: ["VBIAS"],
  pin4: ["C_CC1"],
  pin5: ["C_CC2"],
  pin6: ["RPD_G2"],
  pin7: ["RPD_G1"],
  pin8: ["GND3"],
  pin9: ["N_FLT"],
  pin10: ["VPWR"],
  pin11: ["CC2"],
  pin12: ["CC1"],
  pin13: ["GND2"],
  pin14: ["SBU2"],
  pin15: ["SUB1"],
  pin16: ["N_C2"],
  pin17: ["N_C1"],
  pin18: ["GND1"],
  pin19: ["D2"],
  pin20: ["D1"],
  pin21: ["PAD"]
} as const

const pinAttributes = {
  pin8: {requiresGround: true},
  pin13: {requiresGround: true},
  pin18: {requiresGround: true}
} as const

export const TPD6S300ARUKR = (props: ChipProps<typeof pinLabels>) => {
  return (
    <chip
      pinLabels={pinLabels}
      pinAttributes={pinAttributes}
      supplierPartNumbers={{
  "jlcpcb": [
    "C2876380"
  ]
}}
      manufacturerPartNumber="TPD6S300ARUKR"
      footprint={<footprint>
        <smtpad portHints={["pin21"]} pcbX="-0.000127mm" pcbY="0.000127mm" width="1.6999966mm" height="1.6999966mm" shape="rect" />
<smtpad portHints={["pin20"]} pcbX="-0.799973mm" pcbY="1.499997mm" width="0.1999996mm" height="0.7999984mm" shape="rect" />
<smtpad portHints={["pin19"]} pcbX="-0.399923mm" pcbY="1.499997mm" width="0.1999996mm" height="0.7999984mm" shape="rect" />
<smtpad portHints={["pin18"]} pcbX="0.000127mm" pcbY="1.499997mm" width="0.1999996mm" height="0.7999984mm" shape="rect" />
<smtpad portHints={["pin17"]} pcbX="0.399923mm" pcbY="1.499997mm" width="0.1999996mm" height="0.7999984mm" shape="rect" />
<smtpad portHints={["pin16"]} pcbX="0.799973mm" pcbY="1.499997mm" width="0.1999996mm" height="0.7999984mm" shape="rect" />
<smtpad portHints={["pin15"]} pcbX="1.499997mm" pcbY="0.800227mm" width="0.7999984mm" height="0.1999996mm" shape="rect" />
<smtpad portHints={["pin14"]} pcbX="1.499997mm" pcbY="0.400177mm" width="0.7999984mm" height="0.1999996mm" shape="rect" />
<smtpad portHints={["pin13"]} pcbX="1.499997mm" pcbY="0.000127mm" width="0.7999984mm" height="0.1999996mm" shape="rect" />
<smtpad portHints={["pin12"]} pcbX="1.499997mm" pcbY="-0.399923mm" width="0.7999984mm" height="0.1999996mm" shape="rect" />
<smtpad portHints={["pin11"]} pcbX="1.499997mm" pcbY="-0.799973mm" width="0.7999984mm" height="0.1999996mm" shape="rect" />
<smtpad portHints={["pin10"]} pcbX="0.799719mm" pcbY="-1.499997mm" width="0.1999996mm" height="0.7999984mm" shape="rect" />
<smtpad portHints={["pin9"]} pcbX="0.399669mm" pcbY="-1.499997mm" width="0.1999996mm" height="0.7999984mm" shape="rect" />
<smtpad portHints={["pin8"]} pcbX="-0.000127mm" pcbY="-1.499997mm" width="0.1999996mm" height="0.7999984mm" shape="rect" />
<smtpad portHints={["pin7"]} pcbX="-0.400177mm" pcbY="-1.499997mm" width="0.1999996mm" height="0.7999984mm" shape="rect" />
<smtpad portHints={["pin6"]} pcbX="-0.800227mm" pcbY="-1.499997mm" width="0.1999996mm" height="0.7999984mm" shape="rect" />
<smtpad portHints={["pin5"]} pcbX="-1.499997mm" pcbY="-0.799973mm" width="0.7999984mm" height="0.1999996mm" shape="rect" />
<smtpad portHints={["pin4"]} pcbX="-1.499997mm" pcbY="-0.399923mm" width="0.7999984mm" height="0.1999996mm" shape="rect" />
<smtpad portHints={["pin3"]} pcbX="-1.499997mm" pcbY="0.000127mm" width="0.7999984mm" height="0.1999996mm" shape="rect" />
<smtpad portHints={["pin2"]} pcbX="-1.499997mm" pcbY="0.400177mm" width="0.7999984mm" height="0.1999996mm" shape="rect" />
<smtpad portHints={["pin1"]} pcbX="-1.499997mm" pcbY="0.800227mm" width="0.7999984mm" height="0.1999996mm" shape="rect" />
<silkscreenpath route={[{"x":-1.0001249999999118,"y":-1.5498063999999658},{"x":-1.550060399999893,"y":-1.5498063999999658},{"x":-1.550060399999893,"y":-0.9998710000000983}]} />
<silkscreenpath route={[{"x":1.5498064000000795,"y":-0.9498330000000124},{"x":1.5498064000000795,"y":-1.5498063999999658},{"x":0.9998710000000983,"y":-1.5498063999999658}]} />
<silkscreenpath route={[{"x":0.9998710000000983,"y":1.550060399999893},{"x":1.5498064000000795,"y":1.550060399999893},{"x":1.5498064000000795,"y":1.0001249999999118}]} />
<silkscreenpath route={[{"x":-1.1002263999999968,"y":1.550060399999893},{"x":-1.550060399999893,"y":1.550060399999893},{"x":-1.550060399999893,"y":1.050162999999884}]} />
<silkscreencircle pcbX="-1.904873mm" pcbY="1.396873mm" radius="0.100076mm" />
<silkscreentext text="{NAME}" pcbX="-0.050927mm" pcbY="2.905127mm" anchorAlignment="center" fontSize="1mm" />
<courtyardoutline outline={[{"x":-2.1499962000000323,"y":2.1499962000000323},{"x":2.1499962000000323,"y":2.1499962000000323},{"x":2.1499962000000323,"y":-2.1499962000000323},{"x":-2.1499962000000323,"y":-2.1499962000000323},{"x":-2.1499962000000323,"y":2.1499962000000323}]} />
      </footprint>}
      cadModel={{
        objUrl: objPath,
        stepUrl: stepPath,
        pcbRotationOffset: 270,
        modelOriginPosition: { x: 0, y: 0, z: 0 },
      }}
      {...props}
    />
  )
}