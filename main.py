# This file is for strategy

from util.objects import *
from util.routines import *
from util.tools import find_hits


class Bot(GoslingAgent):
    # This function runs every in-game tick (every time the game updates anything)
    def run(self):
        if self.intent is not None:
            return
        d1 = abs(self.ball.location.y - self.foe_goal.location.y)
        d2 = abs(self.me.location.y - self.foe_goal.location.y)
        is_in_front_of_ball = d1>d2
        if self.kickoff_flag: 
             # set_intent tells the bot what it's trying to do
            self.set_intent(kickoff())
            return
            # if we're in front of the ball retreat
        if is_in_front_of_ball == False:
                self.set_intent(goto(self.friend_goal.location))
                return
         self.set_intent(short_shot(self.foe_goal.location))
        targets = (
            'at_opponent_goal': (self.foe_goal.left_post, self.foe_goal.right_post)
            'away_from_our_net': (self.friend_goal.right_post, self.friend_goal.left_post)
        )
        hits = find_hits(self,targets)
        if len(hits['at_opponent_goal']) > 0:
            self.set_intent(hits['at_opponent_goal'][0])
            return
        if len(hits['away_from_our_net']) > 0:
            self.set_intent(hits['away_from_our_net'][0])
            return
        
        if self.me.boost > 99:
            self.set_intent(short_shot(self.foe_goal.location))
            return
        
        available_boosts = [boost for boost in self.boosts if boost.large and boost.active]
        closest_boost = None
        closest_distance = 10000
        for boosts in available_boosts:
            distance = (self.me.location - boost.location).magnitude()
            if closest_boost is None or distance < closest_distance:
                closest_boost = boost
                closest_distance = distance
        if closest_boost is not None:
            self.set_intent(goto(closest_boost.location))
            return

       

    
