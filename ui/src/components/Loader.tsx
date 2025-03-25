import styled from "styled-components";

export const Loader = () => {
  return (
    <StyledComponent>
      <span className="loader"></span>
    </StyledComponent>
  );
};

const StyledComponent = styled.div`
  .loader {
    width: 215px;
    height: 215px;
    display: block;
    margin: auto;
    position: relative;
    background: #030303;
    box-sizing: border-box;
  }

  .loader::after {
    content: "";
    width: calc(100% - 30px);
    height: calc(100% - 15px);
    top: 15px;
    left: 15px;
    position: absolute;
    background-image: linear-gradient(
        90deg,
        transparent,
        rgba(255, 255, 255, 0.5) 50%,
        transparent 100%
      ),
      linear-gradient(#ddd 100px, transparent 0),
      linear-gradient(#ddd 16px, transparent 0),
      linear-gradient(#ddd 50px, transparent 0);
    background-repeat: no-repeat;
    background-size: 75px 175px, 100% 100px, 100% 16px, 100% 30px;
    background-position: -185px 0, center 0, center 115px, center 142px;
    box-sizing: border-box;
    animation: animloader 1s linear infinite;
  }

  @keyframes animloader {
    to {
      background-position: 185px 0, center 0, center 115px, center 142px;
    }
  }
`;
