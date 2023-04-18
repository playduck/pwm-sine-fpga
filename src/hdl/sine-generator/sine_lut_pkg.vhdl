library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use ieee.math_real.all;

-- This package contains the pre-calculated sine wave LUT
package sine_lut_pkg is
    generic (
        BIT_DEPTH     : integer := 8;
        SAMPLE_AMOUNT : natural := 16
    );

    -- the LUT consists of SAMPLE_AMOUNT entries where each has a size of BIT_DEPTH
    type lut_t is array (0 to SAMPLE_AMOUNT - 1) of std_logic_vector(BIT_DEPTH - 1 downto 0);
    function generate_lut return lut_t;

    -- generate a LUT for this packes's instance
    constant LUT_C : lut_t := generate_lut;

end sine_lut_pkg;

package body sine_lut_pkg is

    function generate_lut return lut_t is
        variable lut_v : lut_t;
    begin
        -- loop through all samples and generate each one
        for i in 0 to SAMPLE_AMOUNT - 1 loop
            -- each sample is constructed using: (sine wave * scale + offset)
            -- the sine wave is scaled to omega=1/2pi to get the first quarter wave only
            lut_v(i) := std_logic_vector(to_unsigned(integer(round(
            (sin(0.5 * MATH_PI * (real(i) + 0.5)/real(SAMPLE_AMOUNT))) * -- sine wave
            real(2 ** (BIT_DEPTH - 1) - 1) +                             -- scale
            real(2 ** (BIT_DEPTH - 1))                                   -- offset
            )), BIT_DEPTH));
        end loop;
        return lut_v;
    end generate_lut;

end;

-- end sine_lut
