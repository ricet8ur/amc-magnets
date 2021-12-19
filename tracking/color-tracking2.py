
import cv2
import argparse
import numpy as np
import math

sz = 0.25
vid_dt = 10
real_dt=1/120

def get_arguments():
    ap = argparse.ArgumentParser()
    ap.add_argument('-f', '--filter', required=False,
                    help='Range filter. RGB or HSV')
    ap.add_argument('-w', '--video', required=False,
                    help='Use file')
    args = vars(ap.parse_args())

    if (not args['filter']) or (not args['filter'].upper() in ['RGB', 'HSV']):
        args['filter'] = 'RGB'
    if not args['video']:
        args['video'] = 'test2.mp4'

    return args


trackers = []


def callback(value):
    # create conf
    if len(trackers)>1:
        with open('color-tracking-conf.txt', 'w') as f:
            range_filter = get_arguments()['filter'].upper()
            for tracker_bar in trackers:
                f.write(str(tracker_bar.n)+' ')
                for x in tracker_bar.get_trackbar_values(range_filter):
                    f.write(str(x)+' ')
                f.write('\n')


class tracker:
    n = 0
    range_filter = 'RGB'

    def __init__(self, n,pos=(10,10), range_filter='RGB'):
        self.n = n
        self.range_filter = range_filter
        #  setup windows pos
        cv2.namedWindow("Trackbars"+str(n), 0)
        cv2.moveWindow('Trackbars'+str(n), int(pos[0]), int(pos[1]))

        # load conf
        conf = []
        with open('color-tracking-conf.txt', 'r') as f:
            if f.readable():
                g = f.readlines()
                p = [x for x in g if x.split()[0] == str(n)]
                if p:
                    conf = [int(x) for x in p[0].split()[1:]]

        id = 0
        for i in ["MIN", "MAX"]:
            v = 0 if i == "MIN" else 255

            for j in range_filter:
                if conf:
                    cv2.createTrackbar("%s_%s" % (
                        j, i), "Trackbars"+str(n), conf[id], 255, callback)
                    id += 1
                else:
                    cv2.createTrackbar("%s_%s" % (
                        j, i), "Trackbars"+str(n), v, 255, callback)

    def get_trackbar_values(self, range_filter):
        values = []

        for i in ["MIN", "MAX"]:
            for j in range_filter:
                v = cv2.getTrackbarPos("%s_%s" % (
                    j, i), "Trackbars"+str(self.n))
                values.append(v)
        return values

    def render(self):
        back = np.zeros((512, 512, 3), dtype="uint8")
        v1_min, v2_min, v3_min, v1_max, v2_max, v3_max = self.get_trackbar_values(
            self.range_filter)
        back[:, :] = ((v3_min+v3_max)//2, (v2_min+v2_max) //
                      2, (v1_min+v1_max)//2)
        cv2.imshow("Trackbars"+str(self.n),back)
   
def main():
    args = get_arguments()
    range_filter = args['filter'].upper()
    w = args['video']

    camera = cv2.VideoCapture(w)
    data_buf = []
    dual_data_buf=[]
    real_time=0
    
    trackers.append(tracker(0,(10,10), range_filter))
    # greeen lineal|ruler
    trackers.append(tracker(1,(800,10), range_filter))

    s = True
    nextimage=False
    while True:
        if s or nextimage:
            nextimage = False
            if args['video']:
                ret, image = camera.read()
                real_time+=real_dt
                if not ret:
                    print('the end of the file')
                    break
                
                rk=0.3
                image = cv2.resize(image, (int(1200*rk),int(720*rk) ), fx=0, fy=0,
                                   interpolation=cv2.INTER_CUBIC)

                if range_filter == 'RGB':
                    frame_to_thresh = image.copy()
                else:
                    frame_to_thresh = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        v1_min, v2_min, v3_min, v1_max, v2_max, v3_max = trackers[0].get_trackbar_values(
            range_filter)
        # print(v1_min, v2_min, v3_min, v1_max, v2_max, v3_max)
        thresh = cv2.inRange(
            frame_to_thresh, (v1_min, v2_min, v3_min), (v1_max, v2_max, v3_max))
        kernel = np.ones((1, 1), np.uint8)
        mask = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        v=trackers[1].get_trackbar_values(range_filter)
        vthresh = cv2.inRange(
            frame_to_thresh, (v[0], v[1], v[2]), (v[3], v[4], v[5]))
        vmask = cv2.morphologyEx(vthresh, cv2.MORPH_OPEN, kernel)
        vmask = cv2.morphologyEx(vmask, cv2.MORPH_CLOSE, kernel)

        # find contours in the mask and initialize the current
        # (x, y) center of the ball
        cnts = cv2.findContours(
            mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        vcnts = cv2.findContours(
            vmask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        # only proceed if at least one contour was found
        q = 10
        vbox=[]

        if len(vcnts) > 0:
            c = max(vcnts, key=cv2.contourArea)
            # get rotated rectangle from outer contour
            rotrect = cv2.minAreaRect(c)
            box = cv2.boxPoints(rotrect)
            box = np.int0(box)
            vbox.append(box)
            # print(box)
            l=lambda a,b: (a**2+b**2)**0.5
            m = max([l(box[x][0]-box[x+1][0],box[x][1]-box[x+1][1]) for x in range(0,3)])
            # print(m)
            q = sz / m
            # draw rotated rectangle on copy of img as result
            # result = image.copy()
            cv2.drawContours(image,[box],0,(0,125,0),2)

            # get angle from rotated rectangle
            angle = rotrect[-1]

            # from https://www.pyimagesearch.com/2017/02/20/text-skew-correction-opencv-python/
            # the `cv2.minAreaRect` function returns values in the
            # range [-90, 0); as the rectangle rotates clockwise the
            # returned angle trends to 0 -- in this special case we
            # need to add 90 degrees to the angle
            if angle < -45:
                angle = -(90 + angle)

            # otherwise, just take the inverse of the angle to make
            # it positive
            else:
                angle = -angle

            # print(box)

            ((x, y), radius) = cv2.minEnclosingCircle(c)
            # if 50<radius:
                    # draw the circle and centroid on the frame,
                    # then update the list of tracked points
                    # cv2.circle(image, (int(x), int(y)),
                    #            int(radius), (100, 0, 0), 2)
                    # cv2.circle(image, (int(x),int(y)), 3, (0, 0, 0), -1)
                    # cv2.putText(
                        # image, "b", (int(x+10), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 0, 0), 1)
                    # cv2.putText(image, "("+str(int(x))+","+str(int(y))+")", (int(x) +
                                # 10, int(y)+15), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 0, 0), 1)

      
        if len(cnts) > 0:
           # print(cnts[0])

            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid
            # print(cnts)
            c_arr = sorted(cnts, key=cv2.contourArea)

            c = c_arr[-1]
            ((x, y), radius) = cv2.minEnclosingCircle(c)

            c2=c
            if len(c_arr)>1:
                c2 = c_arr[-2]
                if s or nextimage:
                    ((x2, y2), radius2) = cv2.minEnclosingCircle(c2)
                    # dual_data_buf.append((real_time,(x,y),(x2,y2)))
                    data_buf.append((real_time,x2,y2,vbox))
                    # if len(dual_data_buf) > 1:
                    #     a, b = dual_data_buf[-1], dual_data_buf[-2]
                    #     w1 = tuple(a[1][x]-a[2][x] for x in range(2))
                    #     w2 = tuple(b[1][x]-b[2][x] for x in range(2))
                    #     if w1!=w2:
                    #         # print(w1,w2)
                    #         cophi = (w1[0]*w2[0]+w1[1]*w2[1])/((w1[0]**2+w1[1]**2)**0.5*(w2[0]**2+w2[1]**2)**0.5)
                    #         phi = max(math.acos(cophi),math.pi-math.acos(cophi))
                    #         print( phi/((a[0]-b[0])*2*math.pi))

            # idk
            # M = cv2.moments(c)
            # center = 0, 0
            # if M["m00"] != 0:
                # center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

            # only proceed if the radius meets a size
            if 0<radius < 20:
                if s or nextimage:
                    data_buf.append((real_time,x,y,vbox))
                    if len(data_buf) >1:
                        a,b=data_buf[-1],data_buf[-2]
                        # velocity
                        # vel = q/(a[0]-b[0])*((a[1]-b[1])**2+(a[2]-b[2])**2)**0.5
                        # print(vel)


                # draw the circle and centroid on the frame,
                # then update the list of tracked points

                cv2.circle(image, (int(x), int(y)),
                           int(radius), (100, 0, 0), 2)
                cv2.circle(image, (int(x),int(y)), 3, (0, 0, 0), -1)

                # cv2.putText(
                    # image, "a", (int(x+10), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (150, 0, 0), 1)
                # cv2.putText(image, "("+str(int(x))+","+str(int(y))+")", (int(x) +
                            # 10, int(y)+15), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (150, 0, 0), 1)

        # show the frame to our screen
        cv2.imshow("Original", image)
        cv2.imshow("Mask1", mask)
        cv2.imshow("Mask2", vmask)
        cv2.moveWindow('Original', 10+400,10+300)
        cv2.moveWindow('Mask1', 10,10+380)
        cv2.moveWindow('Mask2', 10+540,10+380)

        for p in data_buf:
            cv2.circle(image, (int(p[1]), int(p[2])),
                       1, (50, 0, 0), 2)

        for trackbar in trackers:
            trackbar.render()

        k = cv2.waitKey(vid_dt) & 0xFF
        if k is ord('q'):
            break

        elif k is ord('s'):
            if s:
                s = False
            else:
                s = True
        elif k is ord('n'):
            nextimage=True

    f=open('tracks/'+'/'.join(args['video'].split('/')[-2:]).replace('.mp4','.txt'),'w')
    for x in data_buf:
        f.write(' '.join([str(round(y,3))for y in x[:-1]]))
        f.write(' '+' '.join([' '.join(' '.join(str(q)for q in p) for p in y)for y in x[-1]]))
        f.write('\n')

if __name__ == '__main__':
    main()
