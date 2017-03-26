#coding=utf8
from pybloom import BloomFilter, ScalableBloomFilter


f = BloomFilter(capacity=100, error_rate=0.001)

for i in xrange(0, 99):
    for i in xrange(0, 99):
        if f.add(i) == False:
            print 'False'

# print (1.0 - (len(f) / float(f.capacity))) <= f.error_rate + 2e-18
#
# sbf = ScalableBloomFilter(mode=ScalableBloomFilter.SMALL_SET_GROWTH)
# for i in xrange(0, 100):
#     sbf.add(i)
# # print sbf.error_rate
# # print len(sbf)
# # print sbf.error_rate + 2e-18
# print (1.0 - (len(sbf) / float(100))) <= sbf.error_rate + 2e-18

if __name__ == "__main__":
    pass