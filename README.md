# ML For Video Compression
Algorithms for codec compression for both real time streaming and short video creation. Compatible for mobile and web. 


There are several ways to compress videos sent over a network, AVC, HEVC being the most commonly used standards for video codec. 
There are two options for encode-decode , one is to  use software encoders and reduce the burden on the phones resources - GPU, CPU
or to use hardware encoders. One offers better video quality for higher throughput and the latter is higher compression and lower publish latency.
Ultimately its a tradeoff between higher video quality and publish duration.Some of the popular algorithms used for compression are targetted at
reducing the file size of the video and to dynamically switch bitrates based on network speed, video content, user profile and encoding transcoding ladder history.
We have learned from a series of A/B experiments that short video are more susceptible to video quality as there is widespread use of effects and filters that typically
tend to cause some level of degradation to the video quality. Longer videos lead to longer file sizes and exhibit higher sensitivity to publish time, any methods that 
could help reduce the file size in form of higher compression even at the expense of trading few points of VMAF,VQScore Video Quality is acceptable.

##Encoding with Network Speed Calibration
To this effect we investigated an algorithm that dynamically detect upload speed as we observed that some of the regions with poor network conditions and poor quality hardware phones have issues with video creation as well as video viewing.

##Dynamic Encoding with Saliency Mask
We also implemented ways to be able to selectively alter the bitrate based on saliency mask, a concept in computer vision 
where in the face and prominent features are provided higher bitrate than the background and less relevant aspects of the video, a dynamic approach to encoding based on video content.
