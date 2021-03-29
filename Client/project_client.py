import grpc
import pandas
import redis
import time
import project_pb2 as  pb2
import project_pb2_grpc as pb2_grpc




def run():
    channel =grpc.insecure_channel('project_server:50051')
    stub = pb2_grpc.StreamServiceStub(channel)
    request = pb2.streamRequest()
    response = stub.FetchResponse(request)

   #fixed stuff------------
    total_posts = 0
    b=["none","none",0,"none"]
    highest_rated = 0
    lowest_rated = 0
    top3_most_comments=[b,b,b]
    total_score=0
    highest_awarded = 0

    average_score = 0
    conn = redis.StrictRedis(host='project', port=6379)

    #rolling stuff-------------
    rolling_counter = 0
    rolling_total= 0
    rolling_total_comments = 0
    rolling_avg_comments = 0

    for i in response:
        if rolling_counter==360:
            rolling_avg_comments = rolling_total_comments/rolling_total
            print("\n \n AVERGE COMMENT AMOUNT FOR POSTS IN LAST 3 MINUTES \n")
            print(rolling_avg_comments)
            print("\n \n")
            rolling_total = 0
            rolling_total_comments = 0
            rolling_counter = 0
        #counting up for various analytics:
        rolling_total = rolling_total + 1
        rolling_total_comments = rolling_total_comments+i.num_comments

        total_posts = total_posts+1
        total_score = total_score+i.score
        average_score = total_score/total_posts

        if i.score>highest_rated:
            highest_rated=i.score

        if i.score < lowest_rated:
            lowest_rated = i.score

        if i.total_awards > highest_awarded:
            highest_awarded= i.total_awards

        t=0
        while t<2:
            kz = top3_most_comments[t]
            tz = ["none","none",0,"none"]
            if kz[2]< i.num_comments:
                tz[0]=i.postid
                tz[1]=i.title
                tz[2]=i.num_comments
                tz[3]=i.author
                if t==0:
                    top3_most_comments[t+2] = top3_most_comments[t+1]
                    top3_most_comments[t + 1] = top3_most_comments[t]
                if t==1:
                    top3_most_comments[t + 1] = top3_most_comments[t]

                top3_most_comments[t]=tz
                if len(top3_most_comments)>3:
                    le= len(top3_most_comments)
                    while le>2:
                        top3_most_comments.pop(le)
                        le=le-1
                break
            else:
                t=t+1
        print("\n")
        print("TOP 3 POSTS WITH HIGHEST COMMENT AMOUNT")
        print(top3_most_comments)
        print("\n")
        print("CURRENT HIGHEST RATED POST")
        print("Highest Rating", highest_rated)
        print("CURRENT AVERAGE POST RATING")
        print("average score", average_score)
        print("CURRENT LOWEST POST RATING")
        print("Lowest score", lowest_rated)
        print("POST WITH THE HIGHEST NUMBER OF AWARDS HAS")
        print("Num AWARDS", highest_awarded)

        rolling_counter = rolling_counter+1
        print("ROLLING COUNTER", str(rolling_counter))
        output_file = "./outputFile/result.txt"

        with open(output_file, "w") as outfile:
            kasda= 0
            while kasda<len(top3_most_comments):
                outfile.write("TOP 3 POSTS WITH HIGHEST COMMENT AMOUNT \n" +str(top3_most_comments[kasda]) )
                kasda=kasda+1
            outfile.write("CURRENT HIGHEST RATED POST \n" + str(highest_rated))
            outfile.write("CURRENT AVERAGE POST RATING \n" + str(average_score))
            outfile.write("CURRENT LOWEST POST RATING \n" + str(lowest_rated))
            outfile.write("POST WITH THE HIGHEST NUMBER OF AWARDS HAS \n" + str(highest_awarded))
            outfile.close()

if __name__ == '__main__':
    time.sleep(5.0)
    run()

