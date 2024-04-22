<<<<<<< HEAD
﻿using System;
=======
using System;
>>>>>>> e07ee9886051c1b6bd13568b778a6a6de39b6297
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace tetris_
{
    public abstract class Block
    {
        protected abstract Position[][] Tiles { get; }

        protected abstract Position StartOffset { get; }

        public abstract int Id { get; }

        private int rotationState;
<<<<<<< HEAD
        private Position offset;

        public Block()
=======
        private readonly Position offset;

        protected Block()
>>>>>>> e07ee9886051c1b6bd13568b778a6a6de39b6297
        {
            offset = new Position(StartOffset.Row, StartOffset.Column);
        }

        public IEnumerable<Position> TilePositions()
        {
            foreach (Position p in Tiles[rotationState]) 
            {
                yield return new Position(p.Row + offset.Row, p.Column + offset.Column);
            }
        }

        public void RotateCW()
        {
            rotationState = (rotationState + 1) % Tiles.Length;
        }

        public void RotateCCW()
        {
            if (rotationState == 0) rotationState = (rotationState + 4 - 1) % 4;
            else rotationState--;
        }

        public void Move(int rows,  int columns)
        {
            offset.Row += rows;
            offset.Column += columns;
        }

        public void Reset()
        {
            rotationState = 0;
            offset.Row = StartOffset.Row;
            offset.Column = StartOffset.Column;
        }
    }
}
