import streamlit as st

class LearnMate:
    def __init__(self):
        self.company_name = "LearnMate AI"
        self.problem_statement = ("Traditional educational systems often fail to cater to individual learning needs and paces. "
                                  "Develop an AI-powered learning platform that personalizes educational content, recommendations, "
                                  "and pacing for each student based on their learning style, progress, and performance.")
        self.objective = ("Enhance the educational experience by creating a tailored learning environment that adapts to the unique "
                          "needs of each student, thereby improving engagement and outcomes.")
        self.solution = "LearnMate is an AI-powered platform that personalizes educational content, recommendations, and pacing for each student based on their learning style, progress, and performance."
        self.features = [
            "Adaptive learning paths based on individual student progress and performance.",
            "Personalized content recommendations that match the student's learning style.",
            "Real-time feedback and adjustments to ensure optimal learning efficiency."
        ]
        self.how_it_works = [
            "Assess student's learning style, progress, and performance through initial diagnostics.",
            "Generate personalized learning paths and content recommendations.",
            "Monitor student progress and provide real-time adjustments and feedback.",
            "Ensure continuous improvement with periodic reassessments and updates."
        ]
        self.why_learnmate = [
            "Personalized learning experience tailored to each student's needs.",
            "Adaptive learning paths that evolve with student progress.",
            "Enhanced engagement and academic performance through customized content."
        ]
        self.future_scope = [
            "Integration with various educational tools and platforms.",
            "Expanding personalized learning to a wider range of subjects and age groups.",
            "Enhancing AI algorithms for better adaptability and precision."
        ]
        self.team = {
            "Developed by": "Team LearnMate for Hackathon 2024",
            "Team Members": [
                {
                    "name": "Om Singh",
                    "linkedin": "https://www.linkedin.com/in/om-singh-ds/",
                    "github": "https://github.com/Mandalor-09"
                },
                {
                    "name": "Shaileja Patil",
                    "linkedin": "https://www.linkedin.com/in/shailejapatil/",
                    "github": "https://github.com/Shaileja06"
                }
            ],
            "Special Thanks": [
                "🏢 Prasunethon Company: For providing us a valuable opportunity to showcase our Project."
            ]
        }
        self.thank_you_message = ("Thank you for exploring LearnMate. We hope this tool enhances your educational journey and helps you achieve your goals.\n"
                                  "Best wishes for your future endeavors!\n- Team LearnMate")

    def display_content(self):
        st.sidebar.title(self.company_name)
        
        st.title("LearnMate AI: Personalized Learning Platform 👩‍🎓👨‍🎓")
        st.markdown("## Our Journey 🚀")

        st.markdown("### Problem Statement 📝")
        st.markdown(self.problem_statement)

        st.markdown("### Objective 🎯")
        st.markdown(self.objective)

        st.markdown("### Solution 💡")
        st.markdown(self.solution)

        st.markdown("### Features 🌟")
        for feature in self.features:
            st.markdown(f"- {feature}")

        st.markdown("### How it works 🔄")
        for step in self.how_it_works:
            st.markdown(f"- {step}")

        st.markdown("### Why LearnMate Platform? 🌟")
        for benefit in self.why_learnmate:
            st.markdown(f"- {benefit}")

        st.markdown("### Future Scope 🔮")
        for scope in self.future_scope:
            st.markdown(f"- {scope}")

        st.sidebar.markdown("### Team 👥")
        for key, value in self.team.items():
            if key == "Team Members":
                st.sidebar.markdown(f"**{key}:**")
                for member in value:
                    st.sidebar.markdown(f"- {member['name']} [![LinkedIn](https://img.icons8.com/fluent/30/000000/linkedin.png)]({member['linkedin']}) [![GitHub](https://img.icons8.com/fluent/30/000000/github.png)]({member['github']})")
            elif isinstance(value, list):
                st.sidebar.markdown(f"**{key}:**")
                for item in value:
                    st.sidebar.markdown(f"- {item}")
            else:
                st.sidebar.markdown(f"**{key}:** {value}")

        st.markdown("### Thank You! 🙏")
        st.markdown(self.thank_you_message)

if __name__ == "__main__":
    learnmate = LearnMate()
    learnmate.display_content()
