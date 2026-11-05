import React from 'react'
import {Yageo0603ResistorCandidate,CapacitorLandCandidate,TiDbvCandidate,Ao3400LandCandidate,DualRow8Candidate,TiDrl5Candidate,Coilcraft4mmCandidate} from './footprints'
/** Exact nominal candidates screened using manufacturer specifications and exact supplier listings. This does not
 * qualify DC bias, aging, transients, soldering or supply availability. */
export const passiveCandidates:Record<string,string>={
 'resistor:1k':'RC0603FR-071KL',
 'resistor:1.5k':'RC0603FR-071K5L',
 'resistor:510':'RC0603FR-07510RL',
 'resistor:698':'RT0603BRD07698RL',
 'resistor:383':'RT0603BRD07383RL',
 'resistor:5.3k':'RT0603BRD075K3L',
 'resistor:30.9k':'RT0603BRD0730K9L',
 'resistor:240':'RT0603BRD07240RL',
 'resistor:60k':'RT0603BRD0760KL',
 'resistor:909k':'RT0603BRD07909KL',
 'resistor:60.4k':'RT0603BRD0760K4L',
 'resistor:93.1k':'RT0603BRD0793K1L',
 'resistor:845k':'RT0603BRD07845KL',
 'resistor:200k':'RT0603BRD07200KL',
 'resistor:536k':'RT0603BRD07536KL',
 'resistor:100k':'RT0603BRD07100KL', // .1%, also suitable for ordinary pullups
 'resistor:10k':'RC0603FR-0710KL',
 'resistor:1M':'RC0603FR-071ML',
 'resistor:0':'RC0603JR-070RL', // signal links only; not a power-current jumper
 'capacitor:100nF':'C0603C104K5RACTU',
 'capacitor:1uF':'C0805C105K5RACTU',
 'resistor:10M':'RC0603FR-0710ML',
 'resistor:1.65k':'RT0603BRD071K65L',
 'resistor:3.16k':'RT0603BRD073K16L',
 'resistor:402k':'RT0603BRD07402KL',
 'capacitor:22uF':'C1210C226K4RACTU',
 'capacitor:47nF':'C0603C473K5RACTU',
 'capacitor:3.3nF':'C0603C332J5GACTU',
 'capacitor:10uF':'C1210C106K3RACTU', // 1210 candidate: placement must accommodate larger package
 'capacitor:2.2uF':'C0805C225K5RACTU',
 'capacitor:4.7uF':'C0805C475K3RACTU',
 'capacitor:1nF':'C0603C102J5GACTU',
 'capacitor:120pF':'C0603C121J5GACTU',
 'capacitor:33pF':'C0603C330J5GACTU',
}
const auditedCapSizes:Record<string,"0603"|"0805"|"1210">={"C0603C330J5GACTU":"0603","C0603C104K5RACTU": "0603", "C0603C473K5RACTU": "0603", "C0603C332J5GACTU": "0603", "C0603C102J5GACTU": "0603", "C0603C121J5GACTU": "0603", "C0805C105K5RACTU": "0805", "C0805C225K5RACTU": "0805", "C0805C475K3RACTU": "0805", "C1210C226K4RACTU": "1210", "C1210C106K3RACTU": "1210"}
export const tiDbvCandidates:Record<string,5|6>={SN74LVC1G17DBVR:5,TPS70933DBVR:5,SN74LVC1G02DBVR:5,SN74LVC1G08DBVR:5,TPS3808G01DBVR:6,SN74AXC1T45DBVR:6}
export function sourcePassives(el:any):any {
 if(Array.isArray(el))return el.map(sourcePassives)
 if(!React.isValidElement(el))return el
 const p:any=el.props;const props:any={...p}
 const value=p.resistance??p.capacitance
 const key=String(el.type)+':'+value
 if(!p.manufacturerPartNumber&&passiveCandidates[key])props.manufacturerPartNumber=passiveCandidates[key]
 if(p.name==='R_TEMP_HOT_INPUT')props.manufacturerPartNumber='RT0603BRD0710KL' // thermal comparator requires precision
 if(el.type==='resistor'&&!p.footprint&&/^(RT0603|RC0603)/.test(props.manufacturerPartNumber??''))props.footprint=<Yageo0603ResistorCandidate/> // proposed land geometry, not released
 if(el.type==='capacitor'&&!p.footprint&&auditedCapSizes[props.manufacturerPartNumber])props.footprint=<CapacitorLandCandidate size={auditedCapSizes[props.manufacturerPartNumber]}/>
 if(el.type==='chip'&&!p.footprint&&tiDbvCandidates[props.manufacturerPartNumber])props.footprint=<TiDbvCandidate pins={tiDbvCandidates[props.manufacturerPartNumber]}/>
 if(el.type==='chip'&&!p.footprint&&props.manufacturerPartNumber==='AO3400A')props.footprint=<Ao3400LandCandidate/>
 if(el.type==='chip'&&!p.footprint&&props.manufacturerPartNumber==='TLV9032DR')props.footprint=<DualRow8Candidate kind="TI_D8"/>
 if(el.type==='chip'&&!p.footprint&&props.manufacturerPartNumber==='LTC2954ITS8-1#TRMPBF')props.footprint=<DualRow8Candidate kind="ADI_TS8"/>
 // CAT4104: SOIC8 engineering land reuse, not an onsemi recommended layout.
 if(el.type==='chip'&&!p.footprint&&props.manufacturerPartNumber==='CAT4104V-GT3')props.footprint=<DualRow8Candidate kind="TI_D8"/>
 if(el.type==='chip'&&!p.footprint&&props.manufacturerPartNumber==='TPD3E001DRLR')props.footprint=<TiDrl5Candidate/>
 if(el.type==='inductor'&&!p.footprint&&['XGL4020-102MEC','XGL4020-222MEC','XFL4015-471MEC'].includes(props.manufacturerPartNumber))props.footprint=<Coilcraft4mmCandidate/>
 if(p.children)props.children=React.Children.map(p.children,sourcePassives)
 return React.cloneElement(el,props)
}
