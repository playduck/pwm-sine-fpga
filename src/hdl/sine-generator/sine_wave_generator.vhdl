library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use ieee.math_real.all;

-- this entity generates a sine wave using the pre-calculated LUT
entity sine_wave_generator is
    generic (
        BIT_DEPTH     : natural := 8;
        SAMPLE_AMOUNT : natural := 16
    );
    port (
        clk      : in std_logic;                                -- clock input
        sine_out : out std_logic_vector(BIT_DEPTH - 1 downto 0) -- sine wave output
    );
end sine_wave_generator;

architecture rtl of sine_wave_generator is

    -- instantiate new LUT package
    package sine_lut is new work.sine_lut_pkg
        generic map(
            BIT_DEPTH     => BIT_DEPTH,
            SAMPLE_AMOUNT => SAMPLE_AMOUNT
        );

    -- get LUT
    constant LUT : sine_lut.lut_t := sine_lut.LUT_C;

    -- size of the counter nessacery to reach every sample
    constant COUTNER_SIZE : integer := integer(log2(real(SAMPLE_AMOUNT)));

    -- counter to accumulate the amount of samples we have processed
    signal phase_accumulator : unsigned(COUTNER_SIZE - 1 downto 0) := (others => '0');
    constant all_ones        : unsigned(COUTNER_SIZE - 1 downto 0) := (others => '1');

    -- state to keep track which quadrant of the quarter wave are currently in
    type quadrant_t is (Q0, Q1, Q2, Q3);
    signal quadrant : quadrant_t := Q0; -- start in Q0

begin
    process (clk)
    begin
        if rising_edge(clk) then

            -- have we processed all samples for a quarter wave?
            if phase_accumulator = all_ones then

                -- reset phase accumulator
                phase_accumulator <= (others => '0');

                -- determine new quadrant
                case quadrant is
                    when Q0 =>
                        quadrant <= Q1;
                    when Q1 =>
                        quadrant <= Q2;
                    when Q2 =>
                        quadrant <= Q3;
                    when Q3 =>
                        quadrant <= Q0;
                end case;
            end if;

            -- generate the next sine wave sample by indexing into the pre-calculated LUT
            case quadrant is
                when Q0 =>
                    -- use the LUT directly
                    sine_out <= LUT(to_integer(unsigned(
                        phase_accumulator(COUTNER_SIZE - 1 downto 0)
                        )));
                when Q1 =>
                    -- mirror the LUT
                    sine_out <= LUT(SAMPLE_AMOUNT - 1 - to_integer(unsigned(
                        phase_accumulator(COUTNER_SIZE - 1 downto 0)
                        )));
                when Q2 =>
                    -- invert the LUT
                    sine_out <= not LUT(to_integer(unsigned(
                        phase_accumulator(COUTNER_SIZE - 1 downto 0)
                        )));
                when Q3 =>
                    -- flip and mirror the LUT
                    sine_out <= not LUT(SAMPLE_AMOUNT - 1 - to_integer(unsigned(
                        phase_accumulator(COUTNER_SIZE - 1 downto 0)
                        )));
            end case;

            -- update the phase accumulator
            phase_accumulator <= phase_accumulator + to_unsigned(1, COUTNER_SIZE - 1);

        end if;
    end process;
end rtl;
