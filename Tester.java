class Tester {
	public static int findTotalCount(int[] numbers) {
	     int count = 0;
         int num=2;
        for (int i = 0; i < numbers.length - 1; i++) {
            if (numbers[i] == num && numbers[i + 1] == num) {
                count++;
                while (i < numbers.length - 1 && numbers[i + 1] == num) {
                    i++;
                }
            }
        }
        return count;
	}

	public static void main(String[] args) {
		int[] numbers = { 1, 1, 5, 100, -20, 6, 0, 0 };
		System.out.println("Count of adjacent occurrence: "+findTotalCount(numbers));
	}
} 
 
