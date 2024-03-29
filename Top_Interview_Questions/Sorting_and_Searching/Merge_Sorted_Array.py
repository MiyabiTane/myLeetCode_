class Solution(object):
    def merge(self, nums1, m, nums2, n):
        while n > 0:
            if m <= 0 or nums1[m-1] <= nums2[n-1]:
                nums1[m+n-1] = nums2[n-1]
                n -= 1
            else:
                nums1[m+n-1] = nums1[m-1]
                m -= 1
            # print(nums1)

sol = Solution()
sol.merge([1, 2, 3, 0, 0, 0], 3, [2, 5, 6], 3)
sol.merge([0], 0, [1], 1)