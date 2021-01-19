export const transpose = (arr) => {
    const result = [];
    for (let y = arr[0].length - 1; y >= 0; y--) {
        const row = [];
        result.push(row);
        for (let x = 0; x < arr.length; x++) {
            row.push(arr[x][y])
        }
    }
    return result;
}