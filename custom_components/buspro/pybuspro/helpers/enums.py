from enum import Enum


class SuccessOrFailure(Enum):
    Success = b'\xF8'
    Failure = b'\xF5'


class DeviceType(Enum):
    NotSet = b'\x00\x00'
    SB_DN_6B0_10v = b'\x00\x11'   # Rele varme
    SB_DN_SEC250K = b'\x0B\xE9'   # Sikkerhetsmodul
    SB_CMS_12in1 = b'\x01\x34'    # 12i1
    SB_DN_Logic960 = b'\x04\x53'  # Logikkmodul
    SB_DLP2 = b'\x00\x86'         # DLP
    SB_DLP = b'\x00\x95'          # DLP
    SB_DLP_v2 = b'\x00\x9C'       # DLPv2
    PyBusPro = b'\xFF\xFC'
    SmartHDLTest = b'\xFF\xFD'
    SetupTool = b'\xFF\xFE'
    SB_WS8M = b'\x01\x2B'         # 8 keys panel
    SB_CMS_8in1 = b'\x01\x35'     # 8i1
    SB_DN_DT0601 = b'\x02\x60'    # 6ch Dimmer
    HDL_MDT0601 = b'\x02\x6D'     # 6ch Dimmer ny type
    SB_DN_R0816 = b'\x01\xAC'     # Rele
    SB_DRY_4Z = b'\x00\x77'       # Dry contact
    HDL_MSP07M = b'\x01\x50'      # Sensors in One

    # SB_DN_DT0601 = b'\x00\x9E'    # Universaldimmer 6ch 1A
    # SB_DN_RS232N				    # RS232


class OnOff(Enum):
    OFF = 0
    ON = 255


class SwitchStatusOnOff(Enum):
    OFF = 0
    ON = 1


class OnOffStatus(Enum):
    OFF = 0
    ON = 1


class TemperatureType(Enum):
    Celsius = 0
    Fahrenheit = 1


class TemperatureMode(Enum):
    Normal = 1
    Day = 2
    Night = 3
    Away = 4
    Timer = 5


class OperateCode(Enum):
    NotSet = b'\x00'

    SingleChannelControl = b'\x00\x31'
    SingleChannelControlResponse = b'\x00\x32'
    ReadStatusOfChannels = b'\x00\x33'
    ReadStatusOfChannelsResponse = b'\x00\x34'
    SceneControl = b'\x00\x02'
    SceneControlResponse = b'\x00\x03'
    UniversalSwitchControl = b'\xE0\x1C'
    UniversalSwitchControlResponse = b'\xE0\x1D'

    ReadStatusOfUniversalSwitch = b'\xE0\x18'
    ReadStatusOfUniversalSwitchResponse = b'\xE0\x19'
    BroadcastStatusOfUniversalSwitch = b'\xE0\x17'

    BroadcastSensorStatusResponse = b'\x16\x44'
    ReadSensorStatus = b'\x16\x45'
    ReadSensorStatusResponse = b'\x16\x46'
    BroadcastSensorStatusAutoResponse = b'\x16\x47'

    BroadcastTemperatureResponse = b'\xE3\xE5'

    ReadFloorHeatingStatus = b'\x19\x44'
    ReadFloorHeatingStatusResponse = b'\x19\x45'
    ControlFloorHeatingStatus = b'\x19\x46'
    ControlFloorHeatingStatusResponse = b'\x19\x47'

    ReadDryContactStatus = b'\x15\xCE'
    ReadDryContactStatusResponse = b'\x15\xCF'

    ReadSensorsInOneStatus = b'\x16\x04'
    ReadSensorsInOneStatusResponse = b'\x16\x05'

    """
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    """

    # Scene = b'\x00\x02'
    # Response_Scene = b'\x00\x03'

    TIME_IF_FROM_LOGIC_OR_SECURITY = b'\xDA\x44'

    # b'\x1947'
    # INFO_IF_FROM_12in1__1 = b'\x16\x47'
    INFO_IF_FROM_RELE_10V = b'\xEF\xFF'
    # b'\xF036'

    QUERY_DLP_FROM_SETUP_TOOL_1 = b'\xE0\xE4'  # Ingen data sendes svar sendes sender
    RESPONSE_QUERY_DLP_FROM_SETUP_TOOL_1 = b'\xE0\xE5'
    QUERY_DLP_FROM_SETUP_TOOL_2 = b'\x19\x44'  # Ingen data sendes svar sendes sender			FLOOR HEATING WORKING STATUS
    RESPONSE_QUERY_DLP_FROM_SETUP_TOOL_2 = b'\x19\x45'
    QUERY_DLP_FROM_SETUP_TOOL_3 = b'\x19\x40'  # Ingen data sendes svar sendes sender			FLOOR HEATING
    RESPONSE_QUERY_DLP_FROM_SETUP_TOOL_3 = b'\x19\x41'
    QUERY_DLP_FROM_SETUP_TOOL_4 = b'\x19\x46'  # 0 1 1 23 20 20 20										FLOOR HEATING WORKING STATUS CONTROL
    RESPONSE_QUERY_DLP_FROM_SETUP_TOOL_4 = b'\x19\x47'
    # b'\x19\x48' Temperature request?
    # b'\x19\x49' Temperature request?
    # b'\xE3\xE5' GPRS control answer back

    QUERY_12in1_FROM_SETUP_TOOL_1 = b'\x00\x0E'
    RESPONSE_QUERY_12in1_FROM_SETUP_TOOL_1 = b'\x00\x0F'
    QUERY_12in1_FROM_SETUP_TOOL_2 = b'\xF0\x03'
    RESPONSE_QUERY_12in1_FROM_SETUP_TOOL_2 = b'\xF0\x04'
    QUERY_12in1_FROM_SETUP_TOOL_3 = b'\xDB\x3E'
    RESPONSE_QUERY_12in1_FROM_SETUP_TOOL_3 = b'\xDB\x3F'
    QUERY_12in1_FROM_SETUP_TOOL_4 = b'\x16\x66'
    RESPONSE_QUERY_12in1_FROM_SETUP_TOOL_4 = b'\x16\x67'
    QUERY_12in1_FROM_SETUP_TOOL_5 = b'\x16\x45'
    RESPONSE_QUERY_12in1_FROM_SETUP_TOOL_5 = b'\x16\x46'
    QUERY_12in1_FROM_SETUP_TOOL_6 = b'\x16\x5E'
    RESPONSE_QUERY_12in1_FROM_SETUP_TOOL_6 = b'\x16\x5F'
    QUERY_12in1_FROM_SETUP_TOOL_7 = b'\x16\x41'
    RESPONSE_QUERY_12in1_FROM_SETUP_TOOL_7 = b'\x16\x42'
    QUERY_12in1_FROM_SETUP_TOOL_8 = b'\x16\x6E'
    RESPONSE_QUERY_12in1_FROM_SETUP_TOOL_8 = b'\x16\x6F'
    QUERY_12in1_FROM_SETUP_TOOL_9 = b'\x16\xA9'
    RESPONSE_QUERY_12in1_FROM_SETUP_TOOL_9 = b'\x16\xAA'

    '''
    public enum OperationCode
    {
    NotSet = 0x0,
    
    SingleChannelControl = 0x0031,
    SingleChannelControlResponse = 0x0032,
    ReadStatusOfChannels = 0x0033,
    ReadStatusOfChannelsResponse = 0x0034,
    CurtainControlEnabled = 0xDC23,
    CurtainControlEnabledResponse = 0xDC24,
    DetectAddress = 0xE5F5,
    DetectAddressResponse = 0xE5F6,
    BroadcastStatusOfScene = 0xEFFF,
    IsAddressConflict = 0x0284,
    IsAddressConflictResponse = 0x0285,
    IsDeviceOnline = 0xF065,
    IsDeviceOnlineResponse = 0xF066,
    MakeZones = 0x0006,
    MakeZonesResponse = 0x0007,
    ModifyAddress = 0xE5F7,
    ModifyAddressResponse = 0xE5F8,
    ModifyChannelLoadType = 0xF014,
    ModifyChannelLoadTypeResponse = 0xF015,
    ModifyDelayOfTurnOnChannel = 0xF04F,
    ModifyDelayOfTurnOnChannelResponse = 0xF050,
    ModifyDetailOfASequenceInSpecifiedZone = 0x0016,
    ModifyDetailOfASequenceInSpecifiedZoneResponse = 0x0017,
    ModifyLock = 0x0282,
    ModifyLockResponse = 0x0283,
    ModifyMacAddress = 0xF001,
    ModifyMacAddressResult = 0xF002,
    ModifyRemarkOfSpecifiedSequence = 0xF030,
    ModifyRemarkOfSpecifiedSequenceResponse = 0xF031,
    ModifySafeguardTimeOfChannel = 0xF041,
    ModifySafeguardTimeOfChannelResponse = 0xF042,
    ModifySceneConfiguration = 0x0008,
    ModifySceneConfigurationResponse = 0x0009,
    ModifySceneNoOfEveryZoneWhenPowerOn = 0xF057,
    ModifySceneNoOfEveryZoneWhenPowerOnResponse = 0xF058,
    ModifySettingOfSequenceRunning = 0x0018,
    ModifySettingOfSequenceRunningResponse = 0x0019,
    ModifySubnetIdAndDeviceIdByMacAddress = 0xF005,
    ModifySubnetIdAndDeviceIdByMacAddressResponse = 0xF006, //0xF002 i dokumentasjon, dette er nok feil
    ReadChannelLoadType = 0xF012,
    ReadChannelLoadTypeResponse = 0xF013,
    ReadChannelRemark = 0xF00E,
    ReadChannelRemarkResponse = 0xF00F,
    ReadDelayOfTurnOnChannel = 0xF04D,
    ReadDelayOfTurnOnChannelResponse = 0xF04E,
    ReadDetailOfASequenceInSpecifiedZone = 0x0014,
    ReadDetailOfASequenceInSpecifiedZoneResponse = 0x0015,
    ReadDeviceRemark = 0x000E,
    ReadDeviceRemarkResponse = 0x000F,
    ReadFirmwareVersion = 0xEEFD,
    ReadFirmwareVersionResponse = 0xEEFE,
    ReadLimitOfEveryChannel = 0xF016,
    ReadLimitOfEveryChannelResponse = 0xF017,
    ReadLock = 0x0280,
    ReadLockResponse = 0x0281,
    ReadMacAddress = 0xF003,
    ReadMacAddressResult = 0xF004,
    ReadRemarkOfOneZone = 0xF00A,
    ReadRemarkOfOneZoneResponse = 0xF00B,
    ReadRemarkOfSpecifiedSceneOfSpecifiedZone = 0xF024,
    ReadRemarkOfSpecifiedSceneOfSpecifiedZoneResponse = 0xF025,
    ReadRemarkOfSpecifiedSequence = 0xF028,
    ReadRemarkOfSpecifiedSequenceResponse = 0xF029,
    ReadSafeguardTimeOfChannel = 0xF03F,
    ReadSafeguardTimeOfChannelResponse = 0xF040,
    ReadSceneConfiguration = 0x0000,
    ReadSceneConfigurationResponse = 0x0001,
    ReadSceneNoOfAllZonesRunning = 0xF078,
    ReadSceneNoOfAllZonesRunningResponse = 0xF079,
    ReadSceneNoOfEveryZoneWhenPowerOn = 0xF055,
    ReadSceneNoOfEveryZoneWhenPowerOnResponse = 0xF056,
    ReadSequenceNoOfSpecifiedZoneRunning = 0xE014,
    ReadSequenceNoOfSpecifiedZoneRunningResponse = 0xE015,
    ReadSettingOfSequenceRunning = 0x0012,
    ReadSettingOfSequenceRunningResponse = 0x0013,
    ReadSettingsOfZones = 0x0004,
    ReadSettingsOfZonesResponse = 0x0005,
    ReadTypeOfZoneWhenPowerOn = 0xF051,
    ReadTypeOfZoneWhenPowerOnResponse = 0xF052,
    RequestCurrentSmallPackageFromPcToTargetDevice = 0xDC14,
    RequestCurrentSmallPackageFromPcToTargetDeviceResponse = 0xDC15,
    RequestTotalQtyOfPackagesFromPcToTargetDevice = 0xDC10,
    RequestTotalQtyOfPackagesFromPcToTargetDeviceResponse = 0xDC11,
    ReversingControl = 0xDC1C,
    ReversingControlResponse = 0xDC1D,
    SendSmallPackageFromPcToTargetDevice = 0xDC1A,
    SendSmallPackageFromPcToTargetDeviceResponse = 0xDC1B,
    SendTotalQtyOfPackagesFromPcToTargetDevice = 0xDC16,
    SendTotalQtyOfPackagesFromPcToTargetDeviceResponse = 0xDC17,
    SequenceControl = 0x001A,
    SequenceControlResponse = 0x001B,
    SubnetBroadcastToAllDevices = 0x0288,
    WhichModulesAreProgrammedIntoTheHardwareState = 0x0286,
    WhichModulesAreProgrammedIntoTheHardwareStateResponse = 0x0287,
    WriteChannelRemark = 0xF010,
    WriteChannelRemarkResponse = 0xF011,
    WriteDeviceRemark = 0x0010,
    WriteDeviceRemarkResponse = 0x0011,
    WriteLimitOfEveryChannel = 0xF018,
    WriteLimitOfEveryChannelResponse = 0xF019,
    WriteRemarkOfOneZone = 0xF00C,
    WriteRemarkOfOneZoneResponse = 0xF00D,
    WriteRemarkOfSpecifiedSceneOfSpecifiedZone = 0xF026,
    WriteRemarkOfSpecifiedSceneOfSpecifiedZoneResponse = 0xF027,
    WriteTypeOfZoneWhenPowerOn = 0xF053,
    WriteTypeOfZoneWhenPowerOnResponse = 0xF054,
    
    ReadTemperatureOutside = 0x018C,
    ReadTemperatureOutsideResponse = 0x018D,
    ModifyTemperatureOutside = 0x018E,
    ModifyTemperatureOutsideResponse = 0x018F,
    ReadTemperaturRangeOfSpecifiedLogicBlock = 0xD999,
    ReadTemperaturRangeOfSpecifiedLogicBlockResponse = 0xD99A,
    ModifyTemperaturRangeOfSpecifiedLogicBlock = 0xD997,
    ModifyTemperaturRangeOfSpecifiedLogicBlockResponse = 0xD998,
    ReadCompensationOfBrightness = 0xDA00,
    ReadCompensationOfBrightnessResponse = 0xDA01,
    ModifyCompensationOfBrightness = 0xDA02,
    ModifyCompensationOfBrightnessResponse = 0xDA03,
    ReadSensorsStatus = 0xDB00,
    ReadSensorsStatusResponse = 0xDB01,
    ReadPirSensitivity = 0xD828,
    ReadPirSensitivityResponse = 0xD829,
    ModifydPirSensitivity = 0xD826,
    ModifyPirSensitivityResponse = 0xD827,
    ReadDelayTimeOfPir = 0xD818,
    ReadDelayTimeOfPirResponse = 0xD819,
    ModifyDelayTimeOfPir = 0xD80C,
    ModifyDelayTimeOfPirResponse = 0xD80D,
    ReadCurrentBrightness = 0xD992,
    ReadCurrentBrightnessResponse = 0xD993,
    EnableEditingLogicPage = 0xDB30,
    EnableEditingLogicPageResponse = 0xDB31,
    EnableReadLogicPage = 0xDB32,
    EnableReadLogicPageResponse = 0xDB33,
    WriteRemarkOfLogic = 0xD988,
    WriteRemarkOfLogicResponse = 0xD989,
    ReadRemarkOfLogic = 0xD986,
    ReadRemarkOfLogicResponse = 0xD987,
    UniversalSwitchControl = 0xE01C,
    UniversalSwitchControlResponse = 0xE01D,
    BroadcastSystemDateTime = 0xDA44,
    
    ReadAcCurrentStatus = 0xE0EC,
    ReadAcCurrentStatusResponse = 0xE0ED,
    
    ReadFloorHeatingStatus = 0x1944,
    ReadFloorHeatingStatusResponse = 0x1945,
    
    ReadStatusPir = 0x1645,
    ReadStatusPirResponse = 0x1646,
    
    BroadcastTemperature = 0xE3E5,
    
    ReadTemperature = 0xE3E7,
    ReadTemperatureResponse = 0xE3E8,
    
    BroadcastSensorsStatus = 0x1647,
    
    ReadFloorHeatingSettings = 0x1940,
    ReadFloorHeatingSettingsResponse = 0x1941,
    
    ControlFloorHeatingStatus = 0x1946,
    ControlFloorHeatingStatusResponse = 0x1947,
    
    BroadcastStatusOfSequence = 0xF036,
    
    
    
    
    
    XX_QUERY_DLP_FROM_SETUP_TOOL_1 = 0xE0E4,
    XX_RESPONSE_QUERY_DLP_FROM_SETUP_TOOL_1 = 0xE0E5,
    XX_QUERY_12in1_FROM_SETUP_TOOL_3 = 0xDB3E,
    XX_RESPONSE_QUERY_12in1_FROM_SETUP_TOOL_3 = 0xDB3F,
    XX_QUERY_12in1_FROM_SETUP_TOOL_4 = 0x1666,
    XX_RESPONSE_QUERY_12in1_FROM_SETUP_TOOL_4 = 0x1667,
    XX_QUERY_12in1_FROM_SETUP_TOOL_6 = 0x165E,
    XX_RESPONSE_QUERY_12in1_FROM_SETUP_TOOL_6 = 0x165F,
    XX_QUERY_12in1_FROM_SETUP_TOOL_7 = 0x1641,
    XX_RESPONSE_QUERY_12in1_FROM_SETUP_TOOL_7 = 0x1642,
    XX_QUERY_12in1_FROM_SETUP_TOOL_8 = 0x166E,
    XX_RESPONSE_QUERY_12in1_FROM_SETUP_TOOL_8 = 0x166F,
    XX_QUERY_12in1_FROM_SETUP_TOOL_9 = 0x16A9,
    XX_RESPONSE_QUERY_12in1_FROM_SETUP_TOOL_9 = 0x16AA
    '''

    '''

    
    
    public class Channel
    {
    public enum State
    {
    Off = 0,
    On = 100
    }
    
    public enum Status
    {
    Off = 0,
    On = 1
    }
    }
    
    
    public class Temperature
    {
    public enum Type
    {
    Celsius = 0,
    Fahrenheit = 1
    }
    
    public enum Status
    {
    Off = 0,
    On = 1
    }
    
    public enum Mode
    {
    Normal = 1,
    Day = 2,
    Night = 3,
    Away = 4,
    Timer = 5
    }
    
    public enum Timer
    {
    Day = 0,
    Night = 1
    }
    }
    
    '''

    '''
    public enum DeviceType
    {
    UnknownDevice = 0x0,
    
    RELAY_6B0_10v = 0x0011,			// Rele varme
    SECURITY_SEC250K = 0x0BE9,	// Sikkerhetsmodul
    PIR_12in1 = 0x0134,					// 12i1
    LOGIC_Logic960 = 0x0453,		// Logikkmodul
    DLP_DLP2 = 0x0086,					// DLP
    DLP_DLP = 0x0095,						// DLP
    DLP_DLP_v2 = 0x009C,				// DLPv2
    KEY_WS8M = 0x012B,					// 8 keys panel
    PIR_8in1 = 0x0135,					// 8i1
    DIMMER_DT0601 = 0x0260,			// 6ch Dimmer
    RELAY_R0816 = 0x01AC,				// Rele
    DRY_4Z = 0x0077,						// Input
    
    BusproService = 0xFFFC,
    SmartHDLTest = 0xFFFD,
    SetupTool = 0xFFFE,
    
    //SB_DN_DT0601 = 0x009E,	// Universaldimmer 6ch 1A
    //SB_DN_RS232N						// RS232
    //DIMMER_MDT0601 = 0x0260,
    //RELAY_MR0816 = 0x01AC
    //DIMMER_MD0602 = 0x0,
    //RELAY_MFH06 = 0x0
    }
    '''

    '''
    //	public enum Action
    //	{
    //		NotSet = 0x0,
    
    //		SingleChannelControl = 0x0031
    //	}
    '''