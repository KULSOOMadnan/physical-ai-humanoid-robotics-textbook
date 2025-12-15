import React, { useState } from 'react';
import clsx from 'clsx';
import styles from './Quiz.module.css';

type QuizQuestion = {
  id: number;
  question: string;
  options: string[];
  correctAnswer: number; // Index of the correct option
  explanation?: string;
};

type QuizProps = {
  title: string;
  questions: QuizQuestion[];
};

const Quiz: React.FC<QuizProps> = ({ title, questions }) => {
  const [userAnswers, setUserAnswers] = useState<(number | null)[]>(Array(questions.length).fill(null));
  const [showResults, setShowResults] = useState(false);
  const [revealedAnswers, setRevealedAnswers] = useState<boolean[]>(Array(questions.length).fill(false));

  const handleAnswerSelect = (questionIndex: number, optionIndex: number) => {
    if (showResults) return; // Don't allow changes after submitting

    const newAnswers = [...userAnswers];
    newAnswers[questionIndex] = optionIndex;
    setUserAnswers(newAnswers);
  };

  const handleSubmit = () => {
    setShowResults(true);
  };

  const handleReset = () => {
    setUserAnswers(Array(questions.length).fill(null));
    setShowResults(false);
    setRevealedAnswers(Array(questions.length).fill(false));
  };

  const handleShowAnswer = (questionIndex: number) => {
    const newRevealed = [...revealedAnswers];
    newRevealed[questionIndex] = true;
    setRevealedAnswers(newRevealed);
  };

  const calculateScore = () => {
    return questions.reduce((score, question, index) => {
      return userAnswers[index] === question.correctAnswer ? score + 1 : score;
    }, 0);
  };

  return (
    <div className={styles.quizContainer}>
      <h3>{title}</h3>
      <div className={styles.questionsContainer}>
        {questions.map((question, qIndex) => (
          <div key={question.id} className={styles.questionCard}>
            <div className={styles.questionHeader}>
              <h4>Question {qIndex + 1}: {question.question}</h4>
            </div>

            <div className={styles.optionsContainer}>
              {question.options.map((option, oIndex) => (
                <div
                  key={oIndex}
                  className={clsx(
                    styles.option,
                    userAnswers[qIndex] === oIndex && styles.selected,
                    showResults && oIndex === question.correctAnswer && styles.correct,
                    showResults && userAnswers[qIndex] === oIndex && userAnswers[qIndex] !== question.correctAnswer && styles.incorrect
                  )}
                  onClick={() => !showResults && handleAnswerSelect(qIndex, oIndex)}
                >
                  <input
                    type="radio"
                    id={`q${qIndex}-o${oIndex}`}
                    name={`question-${qIndex}`}
                    checked={userAnswers[qIndex] === oIndex}
                    onChange={() => {}}
                    disabled={showResults}
                    className={styles.radioButton}
                  />
                  <label htmlFor={`q${qIndex}-o${oIndex}`} className={styles.optionLabel}>
                    {option}
                  </label>
                </div>
              ))}
            </div>

            {showResults && (
              <div className={styles.resultSection}>
                {userAnswers[qIndex] === question.correctAnswer ? (
                  <div className={styles.correctMessage}>✓ Correct!</div>
                ) : userAnswers[qIndex] !== null ? (
                  <div className={styles.incorrectMessage}>
                    ✗ Incorrect. The correct answer is: {question.options[question.correctAnswer]}
                  </div>
                ) : (
                  <div className={styles.noAnswerMessage}>
                    No answer selected. The correct answer is: {question.options[question.correctAnswer]}
                  </div>
                )}

                {question.explanation && (
                  <div className={styles.explanation}>
                    <details>
                      <summary>Explanation</summary>
                      <p>{question.explanation}</p>
                    </details>
                  </div>
                )}
              </div>
            )}

            {!showResults && (
              <div className={styles.answerButtonContainer}>
                <button
                  className={styles.showAnswerButton}
                  onClick={() => handleShowAnswer(qIndex)}
                >
                  {revealedAnswers[qIndex] ? 'Hide Answer' : 'Show Answer'}
                </button>
              </div>
            )}

            {revealedAnswers[qIndex] && !showResults && (
              <div className={styles.revealedAnswer}>
                <strong>Answer:</strong> {question.options[question.correctAnswer]}
                {question.explanation && <p><strong>Explanation:</strong> {question.explanation}</p>}
              </div>
            )}
          </div>
        ))}
      </div>

      {!showResults ? (
        <div className={styles.buttonContainer}>
          <button className={styles.submitButton} onClick={handleSubmit}>
            Submit Quiz
          </button>
          <button className={styles.resetButton} onClick={handleReset}>
            Reset
          </button>
        </div>
      ) : (
        <div className={styles.resultsContainer}>
          <h4>Quiz Results</h4>
          <p>Your score: {calculateScore()} out of {questions.length}</p>
          <div className={styles.buttonContainer}>
            <button className={styles.resetButton} onClick={handleReset}>
              Try Again
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default Quiz;