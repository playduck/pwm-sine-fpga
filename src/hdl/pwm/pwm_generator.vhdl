library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity pwm_generator is
    generic (
        BIT_DEPTH : natural := 8
    );
    port (
        clk         : in std_logic; -- input clk
        pulse_width : in std_logic_vector(BIT_DEPTH - 1 downto 0); -- current pulse width input
        pwm_out     : out std_logic := '0'; -- pwm output
        sync_out    : out std_logic := '0'  -- 50% fixed pwm output
    );
end entity;

architecture behavioral of pwm_generator is
    signal counter   : unsigned(BIT_DEPTH - 1 downto 0) := (others => '0');
    signal threshold : unsigned(BIT_DEPTH - 1 downto 0) := (others => '0');

    -- half of the BIT_DEPTH (this equivalent to 2**(BIT_DEPTH-1))
    constant half : unsigned(BIT_DEPTH - 1 downto 0) := to_unsigned(integer(real(2.0 ** (BIT_DEPTH - 1))), BIT_DEPTH);
begin

    -- convert pulse width to unsigned value and scale to range of 0 to 2^BIT_DEPTH-1
    threshold <= resize(unsigned(pulse_width), BIT_DEPTH);

    process (clk)
    begin
        if rising_edge(clk) then
            -- increment counter
            counter <= counter + 1;

            -- sync output always has 50% duty cycle
            if counter < half then
                sync_out <= '1';
            else
                sync_out <= '0';
            end if;

            -- generate PWM output based on counter and threshold
            if counter < threshold then
                pwm_out <= '1';
            else
                pwm_out <= '0';
            end if;

        end if;
    end process;
end architecture;

-- end pwm_generator
