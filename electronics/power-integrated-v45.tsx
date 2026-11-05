import React from 'react'
import {PowerIntegrated} from './power-integrated'
import {McuTestAccessV45} from './mcu-test-access-v45'
export function PowerIntegratedV45(){const prior:any=PowerIntegrated(),debug:any=McuTestAccessV45();return React.cloneElement(prior,{},<>{prior.props.children}{debug.props.children}</>)}
