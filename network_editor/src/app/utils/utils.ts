
/**
 * Rounds up a number to 2 decimal places
 * @param num
 */
export function roundNumber(num: any, decimalPlace = 2): number {
  if (num == null) {
    return;
  }

  if (typeof num === 'string' || num instanceof String) {
    num = Number(num);
  }

  return Number(num.toFixed(decimalPlace));
}
