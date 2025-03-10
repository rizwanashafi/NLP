from crewai.flow.flow import Flow, listen, start, router
from dotenv import load_dotenv
from litellm import completion


class TechFlow(Flow):
    model = "gemini/gemini-1.5-flash"

class RouterFlow(TechFlow):

    @start()
    def generate_city(self):
        # print("Starting flow")
        # print(f"Flow State ID: {self.state['id']}")

        response = completion(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": "Return a list of Pakistan's most populous cities in order (comma-separated).",
                },
            ],
        )

        cities_list = response["choices"][0]["message"]["content"]
        cities = cities_list.split(", ")  # Convert to a list
        self.state["cities"] = cities

        print(f"Most Populous Cities: {cities_list}")
        return cities_list

    @router(generate_city)
    def route_next_step(self):
        """Router to check for Karachi and the next populous city."""
        cities = self.state["cities"]

        if "Karachi" in cities:
            karachi_index = cities.index("Karachi")
            
            # Check if there’s a next city after Karachi
            next_city = cities[karachi_index + 1] if karachi_index + 1 < len(cities) else "No next city"
            
            print(f"Karachi is the most popular city. Next populous city: {next_city}")
            self.state["next_city"] = next_city
            
            return self.generate_fun_fact  # Route if Karachi is found

        return None  # Stop if Karachi is not in the list

    @listen(generate_city)
    def generate_fun_fact(self, cities_list):
        """Generate fun facts about multiple cities."""
        next_city = self.state.get("next_city", "Unknown City")

        response = completion(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": f"Tell me a fun fact about Karachi and also about {next_city}.",
                },
            ],
        )

        fun_fact = response["choices"][0]["message"]["content"]
        self.state["fun_fact"] = fun_fact
        
        print(f"Fun Fact: {fun_fact}")
        return fun_fact


def kickoff():
    flow = RouterFlow()
    flow.kickoff()

def plot():
    flow = RouterFlow()
    flow.plot()

if __name__ == "__main__":
    kickoff()
