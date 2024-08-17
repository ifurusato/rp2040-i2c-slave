I2C_OFFSET = {
    "I2C_IC_CON":            0x00000000,
    "I2C_IC_TAR":            0x00000004,
    "I2C_IC_SAR":            0x00000008,
    "I2C_IC_DATA_CMD":       0x00000010,
    "I2C_IC_SS_SCL_HCNT":    0x00000014,
    "I2C_IC_SS_SCL_LCNT":    0x00000018,
    "I2C_IC_FS_SCL_HCNT":    0x0000001c,
    "I2C_IC_FS_SCL_LCNT":    0x00000020,
    "I2C_IC_INTR_STAT":      0x0000002c,
    "I2C_IC_INTR_MASK":      0x00000030,
    "I2C_IC_RAW_INTR_STAT":  0x00000034,
    "I2C_IC_RX_TL":          0x00000038,
    "I2C_IC_TX_TL":          0x0000003c,
    "I2C_IC_CLR_INTR":       0x00000040,
    "I2C_IC_CLR_RX_UNDER":   0x00000044,
    "I2C_IC_CLR_RX_OVER":    0x00000048,
    "I2C_IC_CLR_TX_OVER":    0x0000004c,
    "I2C_IC_CLR_RD_REQ":     0x00000050,
    "I2C_IC_CLR_TX_ABRT":    0x00000054,
    "I2C_IC_CLR_RX_DONE":    0x00000058,
    "I2C_IC_CLR_ACTIVITY":   0x0000005c,
    "I2C_IC_CLR_STOP_DET":   0x00000060,
    "I2C_IC_CLR_START_DET":  0x00000064,
    "I2C_IC_CLR_GEN_CALL":   0x00000068,
    "I2C_IC_ENABLE":         0x0000006c,
    "I2C_IC_STATUS":         0x00000070,
    "I2C_IC_TXFLR":          0x00000074,
    "I2C_IC_RXFLR":          0x00000078,
    "I2C_IC_SDA_HOLD":       0x0000007c,
    "I2C_IC_TX_ABRT_SOURCE": 0x00000080,
    "I2C_IC_SLV_DATA_NACK_ONLY": 0x00000084,
    "I2C_IC_DMA_CR":             0x00000088,
    "I2C_IC_DMA_TDLR":           0x0000008c,
    "I2C_IC_DMA_RDLR":           0x00000090,
    "I2C_IC_SDA_SETUP":          0x00000094,
    "I2C_IC_ACK_GENERAL_CALL":   0x00000098,
    "I2C_IC_ENABLE_STATUS":      0x0000009c,
    "I2C_IC_FS_SPKLEN":          0x000000a0,
    "I2C_IC_CLR_RESTART_DET":    0x000000a8,
    "I2C_IC_COMP_PARAM_1":       0x000000f4,
    "I2C_IC_COMP_VERSION":       0x000000f8,
    "I2C_IC_COMP_TYPE":          0x000000fc,
}




I2C_IC_CON = {
    0x00000400: "STOP_DET_IF_MASTER_ACTIVE",    # Master issues the STOP_DET interrupt irrespective of whether...
    0x00000200: "RX_FIFO_FULL_HLD_CTRL",        # This bit controls whether DW_apb_i2c should hold the bus when the Rx...
    0x00000100: "TX_EMPTY_CTRL",                # This bit controls the generation of the TX_EMPTY interrupt, as described in...
    0x00000080: "STOP_DET_IFADDRESSED",         # In slave mode: - 1'b1: issues the STOP_DET interrupt only when it is...
    0x00000040: "IC_SLAVE_DISABLE",             # This bit controls whether I2C has its slave disabled, which means once...
    0x00000020: "IC_RESTART_EN",                # Determines whether RESTART conditions may be sent when acting as a master.
    0x00000010: "IC_10BITADDR_MASTER",          # Controls whether the DW_apb_i2c starts its transfers in 7- or 10-bit...
    0x00000008: "IC_10BITADDR_SLAVE",           # When acting as a slave, this bit controls whether the DW_apb_i2c...
    0x00000006: "SPEED",                        # These bits control at which speed the DW_apb_i2c operates; its setting is relevant...
    0x00000001: "MASTER_MODE",                  # This bit controls whether the DW_apb_i2c master is enabled.
}

I2C_IC_TAR = {
    0x00000800: "SPECIAL",                      # This bit indicates whether software performs a Device-ID or General Call or START...
    0x00000400: "GC_OR_START",                  # If bit 11 (SPECIAL) is set to 1 and bit 13(Device-ID) is set to 0, then this...
    0x000003FF: "IC_TAR",                       # This is the target address for any master transaction
}

I2C_IC_SAR = {
    0x000003FF: "IC_SAR",                       # The IC_SAR holds the slave address when the I2C is operating as a slave
}

I2C_IC_DATA_CMD = {
    0x00000800: "FIRST_DATA_BYTE",              # Indicates the first data byte received after the address phase for receive...
    0x00000400: "RESTART",                      # This bit controls whether a RESTART is issued before the byte is sent or received
    0x00000200: "STOP",                         # This bit controls whether a STOP is issued after the byte is sent or received
    0x00000100: "CMD",                          # This bit controls whether a read or a write is performed
    0x000000FF: "DAT",                          # This register contains the data to be transmitted or received on the I2C bus
}

I2C_IC_SS_SCL_HCNT = {
    0x0000FFFF: "IC_SS_SCL_HCNT",               # This register must be set before any I2C bus transaction can take place...
}

I2C_IC_SS_SCL_LCNT = {
    0x0000FFFF: "IC_SS_SCL_LCNT",               # This register must be set before any I2C bus transaction can take place...
}

I2C_IC_FS_SCL_HCNT = {
    0x0000FFFF: "IC_FS_SCL_HCNT",               # This register must be set before any I2C bus transaction can take place...
}

I2C_IC_FS_SCL_LCNT = {
    0x0000FFFF: "IC_FS_SCL_LCNT",               # This register must be set before any I2C bus transaction can take place...
}

I2C_IC_INTR_STAT = {
    0x00001000: "R_RESTART_DET",                # See IC_RAW_INTR_STAT for a detailed description of R_RESTART_DET bit
    0x00000800: "R_GEN_CALL",                   # See IC_RAW_INTR_STAT for a detailed description of R_GEN_CALL bit
    0x00000400: "R_START_DET",                  # See IC_RAW_INTR_STAT for a detailed description of R_START_DET bit
    0x00000200: "R_STOP_DET",                   # See IC_RAW_INTR_STAT for a detailed description of R_STOP_DET bit
    0x00000100: "R_ACTIVITY",                   # See IC_RAW_INTR_STAT for a detailed description of R_ACTIVITY bit
    0x00000080: "R_RX_DONE",                    # See IC_RAW_INTR_STAT for a detailed description of R_RX_DONE bit
    0x00000040: "R_TX_ABRT",                    # See IC_RAW_INTR_STAT for a detailed description of R_TX_ABRT bit
    0x00000020: "R_RD_REQ",                     # See IC_RAW_INTR_STAT for a detailed description of R_RD_REQ bit
    0x00000010: "R_TX_EMPTY",                   # See IC_RAW_INTR_STAT for a detailed description of R_TX_EMPTY bit
    0x00000008: "R_TX_OVER",                    # See IC_RAW_INTR_STAT for a detailed description of R_TX_OVER bit
    0x00000004: "R_RX_FULL",                    # See IC_RAW_INTR_STAT for a detailed description of R_RX_FULL bit
    0x00000002: "R_RX_OVER",                    # See IC_RAW_INTR_STAT for a detailed description of R_RX_OVER bit
    0x00000001: "R_RX_UNDER",                   # See IC_RAW_INTR_STAT for a detailed description of R_RX_UNDER bit
}

I2C_IC_INTR_MASK = {
    0x00001000: "M_RESTART_DET",                # This bit masks the R_RESTART_DET interrupt in IC_INTR_STAT register
    0x00000800: "M_GEN_CALL",                   # This bit masks the R_GEN_CALL interrupt in IC_INTR_STAT register
    0x00000400: "M_START_DET",                  # This bit masks the R_START_DET interrupt in IC_INTR_STAT register
    0x00000200: "M_STOP_DET",                   # This bit masks the R_STOP_DET interrupt in IC_INTR_STAT register
    0x00000100: "M_ACTIVITY",                   # This bit masks the R_ACTIVITY interrupt in IC_INTR_STAT register
    0x00000080: "M_RX_DONE",                    # This bit masks the R_RX_DONE interrupt in IC_INTR_STAT register
    0x00000040: "M_TX_ABRT",                    # This bit masks the R_TX_ABRT interrupt in IC_INTR_STAT register
    0x00000020: "M_RD_REQ",                     # This bit masks the R_RD_REQ interrupt in IC_INTR_STAT register
    0x00000010: "M_TX_EMPTY",                   # This bit masks the R_TX_EMPTY interrupt in IC_INTR_STAT register
    0x00000008: "M_TX_OVER",                    # This bit masks the R_TX_OVER interrupt in IC_INTR_STAT register
    0x00000004: "M_RX_FULL",                    # This bit masks the R_RX_FULL interrupt in IC_INTR_STAT register
    0x00000002: "M_RX_OVER",                    # This bit masks the R_RX_OVER interrupt in IC_INTR_STAT register
    0x00000001: "M_RX_UNDER",                   # This bit masks the R_RX_UNDER interrupt in IC_INTR_STAT register
}

I2C_IC_RAW_INTR_STAT = {
    0x00001000: "RESTART_DET",                  # Indicates whether a RESTART condition has occurred on the I2C interface when...
    0x00000800: "GEN_CALL",                     # Set only when a General Call address is received and it is acknowledged
    0x00000400: "START_DET",                    # Indicates whether a START or RESTART condition has occurred on the I2C interface...
    0x00000200: "STOP_DET",                     # Indicates whether a STOP condition has occurred on the I2C interface regardless...
    0x00000100: "ACTIVITY",                     # This bit captures DW_apb_i2c activity and stays set until it is cleared
    0x00000080: "RX_DONE",                      # When the DW_apb_i2c is acting as a slave-transmitter, this bit is set to 1 if the...
    0x00000040: "TX_ABRT",                      # This bit indicates if DW_apb_i2c, as an I2C transmitter, is unable to complete the...
    0x00000020: "RD_REQ",                       # This bit is set to 1 when DW_apb_i2c is acting as a slave and another I2C master is...
    0x00000010: "TX_EMPTY",                     # The behavior of the TX_EMPTY interrupt status differs based on the TX_EMPTY_CTRL...
    0x00000008: "TX_OVER",                      # Set during transmit if the transmit buffer is filled to IC_TX_BUFFER_DEPTH and the...
    0x00000004: "RX_FULL",                      # Set when the receive buffer reaches or goes above the RX_TL threshold in the...
    0x00000002: "RX_OVER",                      # Set if the receive buffer is completely filled to IC_RX_BUFFER_DEPTH and an...
    0x00000001: "RX_UNDER",                     # Set if the processor attempts to read the receive buffer when it is empty by...
}

I2C_IC_RX_TL = {
    0x000000FF: "RX_TL",                        # Receive FIFO Threshold Level
}

I2C_IC_TX_TL = {
    0x000000FF: "TX_TL",                        # Transmit FIFO Threshold Level
}

I2C_IC_CLR_INTR = {
    0x00000001: "CLR_INTR",                     # Read this register to clear the combined interrupt, all individual interrupts,...
}

I2C_IC_CLR_RX_UNDER = {
    0x00000001: "CLR_RX_UNDER",                 # Read this register to clear the RX_UNDER interrupt (bit 0) of the...
}

I2C_IC_CLR_RX_OVER = {
    0x00000001: "CLR_RX_OVER",                  # Read this register to clear the RX_OVER interrupt (bit 1) of the...
}

I2C_IC_CLR_TX_OVER = {
    0x00000001: "CLR_TX_OVER",                  # Read this register to clear the TX_OVER interrupt (bit 3) of the...
}

I2C_IC_CLR_RD_REQ = {
    0x00000001: "CLR_RD_REQ",                   # Read this register to clear the RD_REQ interrupt (bit 5) of the...
}

I2C_IC_CLR_TX_ABRT = {
    0x00000001: "CLR_TX_ABRT",                  # Read this register to clear the TX_ABRT interrupt (bit 6) of the...
}

I2C_IC_CLR_RX_DONE = {
    0x00000001: "CLR_RX_DONE",                  # Read this register to clear the RX_DONE interrupt (bit 7) of the...
}

I2C_IC_CLR_ACTIVITY = {
    0x00000001: "CLR_ACTIVITY",                 # Reading this register clears the ACTIVITY interrupt if the I2C is not active anymore
}

I2C_IC_CLR_STOP_DET = {
    0x00000001: "CLR_STOP_DET",                 # Read this register to clear the STOP_DET interrupt (bit 9) of the...
}

I2C_IC_CLR_START_DET = {
    0x00000001: "CLR_START_DET",                # Read this register to clear the START_DET interrupt (bit 10) of the...
}

I2C_IC_CLR_GEN_CALL = {
    0x00000001: "CLR_GEN_CALL",                 # Read this register to clear the GEN_CALL interrupt (bit 11) of...
}

I2C_IC_ENABLE = {
    0x00000004: "TX_CMD_BLOCK",                 # In Master mode: - 1'b1: Blocks the transmission of data on I2C bus even if Tx...
    0x00000002: "ABORT",                        # When set, the controller initiates the transfer abort
    0x00000001: "ENABLE",                       # Controls whether the DW_apb_i2c is enabled
}

I2C_IC_STATUS = {
    0x00000040: "SLV_ACTIVITY",                 # Slave FSM Activity Status
    0x00000020: "MST_ACTIVITY",                 # Master FSM Activity Status
    0x00000010: "RFF",                          # Receive FIFO Completely Full
    0x00000008: "RFNE",                         # Receive FIFO Not Empty
    0x00000004: "TFE",                          # Transmit FIFO Completely Empty
    0x00000002: "TFNF",                         # Transmit FIFO Not Full
    0x00000001: "ACTIVITY",                     # I2C Activity Status
}

I2C_IC_TXFLR = {
    0x0000001F: "TXFLR",                        # Transmit FIFO Level
}

I2C_IC_RXFLR = {
    0x0000001F: "RXFLR",                        # Receive FIFO Level
}

I2C_IC_SDA_HOLD = {
    0x00FF0000: "IC_SDA_RX_HOLD",               # Sets the required SDA hold time in units of ic_clk period, when DW_apb_i2c...
    0x0000FFFF: "IC_SDA_TX_HOLD",               # Sets the required SDA hold time in units of ic_clk period, when DW_apb_i2c...
}

I2C_IC_TX_ABRT_SOURCE = {
    0xFF800000: "TX_FLUSH_CNT",                 # This field indicates the number of Tx FIFO Data Commands which are flushed...
    0x00010000: "ABRT_USER_ABRT",               # This is a master-mode-only bit
    0x00008000: "ABRT_SLVRD_INTX",              # 1: When the processor side responds to a slave mode request for data to be...
    0x00004000: "ABRT_SLV_ARBLOST",             # This field indicates that a Slave has lost the bus while transmitting...
    0x00002000: "ABRT_SLVFLUSH_TXFIFO",         # This field specifies that the Slave has received a read command and...
    0x00001000: "ARB_LOST",                     # This field specifies that the Master has lost arbitration, or if...
    0x00000800: "ABRT_MASTER_DIS",              # This field indicates that the User tries to initiate a Master operation...
    0x00000400: "ABRT_10B_RD_NORSTRT",          # This field indicates that the restart is disabled (IC_RESTART_EN bit...
    0x00000200: "ABRT_SBYTE_NORSTRT",           # To clear Bit 9, the source of the ABRT_SBYTE_NORSTRT must be fixed...
    0x00000100: "ABRT_HS_NORSTRT",              # This field indicates that the restart is disabled (IC_RESTART_EN bit...
    0x00000080: "ABRT_SBYTE_ACKDET",            # This field indicates that the Master has sent a START Byte and the START...
    0x00000040: "ABRT_HS_ACKDET",               # This field indicates that the Master is in High Speed mode and the High...
    0x00000020: "ABRT_GCALL_READ",              # This field indicates that DW_apb_i2c in the master mode has sent a General...
    0x00000010: "ABRT_GCALL_NOACK",             # This field indicates that DW_apb_i2c in master mode has sent a General...
    0x00000008: "ABRT_TXDATA_NOACK",            # This field indicates the master-mode only bit
    0x00000004: "ABRT_10ADDR2_NOACK",           # This field indicates that the Master is in 10-bit address mode and that...
    0x00000002: "ABRT_10ADDR1_NOACK",           # This field indicates that the Master is in 10-bit address mode and the...
    0x00000001: "ABRT_7B_ADDR_NOACK",           # This field indicates that the Master is in 7-bit addressing mode and...
}

I2C_IC_SLV_DATA_NACK_ONLY = {
    0x00000001: "NACK",                         # Generate NACK
}

I2C_IC_DMA_CR = {
    0x00000002: "TDMAE",                        # Transmit DMA Enable
    0x00000001: "RDMAE",                        # Receive DMA Enable
}

I2C_IC_DMA_TDLR = {
    0x0000000F: "DMATDL",                       # Transmit Data Level
}

I2C_IC_DMA_RDLR = {
    0x0000000F: "DMARDL",                       # Receive Data Level
}

I2C_IC_SDA_SETUP = {
    0x000000FF: "SDA_SETUP",                    # SDA Setup
}

I2C_IC_ACK_GENERAL_CALL = {
    0x00000001: "ACK_GEN_CALL",                 # ACK General Call
}

I2C_IC_ENABLE_STATUS = {
    0x00000004: "SLV_RX_DATA_LOST",             # Slave Received Data Lost
    0x00000002: "SLV_DISABLED_WHILE_BUSY",      # Slave Disabled While Busy (Transmit, Receive)
    0x00000001: "IC_EN",                        # ic_en Status
}

I2C_IC_FS_SPKLEN = {
    0x000000FF: "IC_FS_SPKLEN",                 # I2C SS, FS or FM+ spike suppression limit
}

I2C_IC_CLR_RESTART_DET = {
    0x00000001: "CLR_RESTART_DET",              # Clear RESTART_DET Interrupt Register
}

I2C_IC_COMP_PARAM_1 = {
    0x00FF0000: "TX_BUFFER_DEPTH",              # TX Buffer Depth = 16
    0x0000FF00: "RX_BUFFER_DEPTH",              # RX Buffer Depth = 16
    0x00000080: "ADD_ENCODED_PARAMS",           # Encoded parameters not visible
    0x00000040: "HAS_DMA",                      # DMA handshaking signals are enabled
    0x00000020: "INTR_IO",                      # COMBINED Interrupt outputs
    0x00000010: "HC_COUNT_VALUES",              # Programmable count values for each mode
    0x0000000C: "MAX_SPEED_MODE",               # MAX SPEED MODE = FAST MODE
    0x00000003: "APB_DATA_WIDTH",               # APB data bus width is 32 bits
}

I2C_IC_COMP_VERSION = {
    0xFFFFFFFF: "IC_COMP_VERSION",              # IC_COMP_VERSION = 0x3230312a
}

I2C_IC_COMP_TYPE = {
    0xFFFFFFFF: "IC_COMP_TYPE",                 # IC_COMP_TYPE = 0x44570140 (Designware Component Type number = 0x44_57_01_40)
}

